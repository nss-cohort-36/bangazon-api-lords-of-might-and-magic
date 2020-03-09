import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazon.models import PaymentType, Customer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from unittest.mock import patch

class TestPaymentType(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user = self.user, is_active=True, city= "Nashville")
        # self.payment_type = PaymentType.objects.create(merchant_name = "bank", customer_id = 1, acct_number = 1234,  expiration_date = '2020-08-10' )

    def test_post_product_type(self):
        # define a park area to be sent to the API
        new_payment_type = {
            "merchant_name" : "bank", 
            "customer_id" : 1, 
            "acct_number" : 1234,  
            "expiration_date" : '2020-08-10'
        }

        #  Use the client to send the request and store the response
        response = self.client.post(
            reverse('paymenttype-list'), new_payment_type, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)

        
        self.assertEqual(PaymentType.objects.count(), 1)

        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(PaymentType.objects.get().merchant_name, 'bank')

    def test_get_payment_type(self):
        new_payment_type = PaymentType.objects.create(merchant_name = "bank", customer_id = 1, acct_number = 1234,  expiration_date = '2020-08-10' )
        

        # Now we can grab all the area (meaning the one we just created) from the db
        response = self.client.get(reverse('paymenttype-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
       
        self.assertEqual(len(response.data), 1)

        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["merchant_name"], "bank")

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(new_payment_type.merchant_name.encode(), response.content)

    def test_delete_payment_type(self):
        new_payment_type = PaymentType.objects.create(merchant_name = "bank", customer_id = 1, acct_number = 1234,  expiration_date = '2020-08-10' )

        response = self.client.delete(
           (reverse('paymenttype-list')+f'/{str(new_payment_type.id)}'), new_payment_type, HTTP_AUTHORIZATION='Token ' + str(self.token), content_type="application/json"
          )

        # Getting 204 back because we have a success url
        self.assertEqual(response.status_code, 204)

        # Query the table to see if there's one ParkArea instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(PaymentType.objects.count(), 0)

        # # And see if it's the one we just added by checking one of the properties. Here, name.
        # self.assertEqual(OrderProduct.objects.get().order_id, 1)
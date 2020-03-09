import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazon.models import Order, Customer, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestOrder(TestCase):
    
    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password, first_name='test', last_name='user')
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(is_active=1, user_id=self.user.id)
        self.payment_type = PaymentType.objects.create(merchant_name="Discover", acct_number="1234567890", expiration_date="2024-01-01", customer_id=1)
    
    def test_post_order(self):
        
        # define a new order to be sent to the API
        new_order = {}
       
        #  Use the client to send the request and store the response
        response = self.client.post(
            reverse('order-list'), new_order, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )
        
        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)
        
        # Query the table to see if there's one Order instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(Order.objects.count(), 1)
        
        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(Order.objects.get().customer_id, 1)

    def test_list_order(self):

        new_order = Order.objects.create(customer_id=1)
        
        response = self.client.get(reverse('order-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)
        
        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one parkarea in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 5)
        
        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data["id"], 1)
        
        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        # I had to add the str() for the id
        self.assertIn(str(new_order.id).encode(), response.content)

    def test_retieve_order(self):

        new_order = Order.objects.create(customer_id=1)

        response = self.client.get(reverse('order-detail', kwargs={'pk': 1}), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)
        
        # making sure that our response is return the correct amount of data
        self.assertEqual(len(response.data), 5)
        
        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data["id"], 1)
        
        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        # I had to add str() for the id check
        self.assertIn(str(new_order.id).encode(), response.content) 

    def test_update_order(self):

        order = Order.objects.create(customer_id=1)
        updated_order = {
            "payment_type_id": self.payment_type.id
        }

        # update and response
        response = self.client.put((reverse('order-list') + f'/1'), updated_order, HTTP_AUTHORIZATION='Token ' + str(self.token), content_type="application/json")

        # looking for 204 response
        self.assertEqual(response.status_code, 204)
        
        # I guess checking that the response doesn't return anything
        self.assertEqual(len(response.data), 0)
        
        # make sure the object we updated has the correct payment type that we added
        self.assertEqual(Order.objects.get().payment_type_id, 1)

    def test_delete_order(self):

        order = Order.objects.create(customer_id=1)

        # delete and response
        response = self.client.delete((reverse('order-detail', kwargs={"pk": 1})), order, HTTP_AUTHORIZATION='Token ' + str(self.token))
        
        # print("response data: ", response.data)

        # checking that the response is 204
        self.assertEqual(response.status_code, 204)
        
        # making sure the response is empty
        self.assertEqual(len(response.data), 0)
        
        # testing that the order object was deleted
        self.assertEqual(Order.objects.count(), 0) 

if __name__ == '__main__':
    unittest.main()
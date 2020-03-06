import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazon.models import OrderProduct, Customer, Product, ProductType, Order
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from unittest.mock import patch

class TestOrderProduct(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user = self.user, is_active=True, city= "Nashville")
        self.product = Product.objects.create(name = "stuff", customer_id = 1, price = 1.00, quantity = 1, description = "more stuff", location = "Nashville", image_path = "image", product_type_id = 1 )
        self.producttype = ProductType.objects.create(name = "type of stuff")
        self.order = Order.objects.create(customer_id = 1)
        self.new_order_product = OrderProduct.objects.create(order_id = 1, product_id = 1)

    def test_patch_order_product(self):
        new_order_product = {
            "order_id": 1,
            "product_id": 1,
        }

        response = self.client.post(
            reverse('orderproduct-list'), new_order_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        # Getting 200 back because we have a success url
        self.assertEqual(response.status_code, 200)

        # Query the table to see if there's one ParkArea instance in there. Since we are testing a POST request, we don't need to test whether an HTTP GET works. So, we just use the ORM to see if the thing we saved is in the db.
        self.assertEqual(OrderProduct.objects.count(), 2)

        # And see if it's the one we just added by checking one of the properties. Here, name.
        self.assertEqual(OrderProduct.objects.get().order_id, 1)

    def test_get_order_product(self):
        new_order_product = OrderProduct.objects.create(
            order_id=1,
            product_id=1,
        )


        

        # Now we can grab all the area (meaning the one we just created) from the db
        response = self.client.get(reverse('orderproduct-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        # Check that the response is 200 OK.
        # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
        self.assertEqual(response.status_code, 200)

        # response.data is the python serialised data used to render the JSON, while response.content is the JSON itself.
        # Are we responding with the data we asked for? There's just one parkarea in our dummy db, so it should contain a list with one instance in it
        self.assertEqual(len(response.data), 2)
        # print(response.data[0]["id"])
        # test the contents of the data before it's serialized into JSON
        self.assertEqual(response.data[0]["id"], 1)

        # Finally, test the actual rendered content as the client would receive it.
        # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
        self.assertIn(self.new_order_product.order_id.encode(), response.content)


if __name__ == '__main__':
    unittest.main()
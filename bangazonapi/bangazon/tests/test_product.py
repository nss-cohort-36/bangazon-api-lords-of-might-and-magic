import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazon.models import Product, Customer, ProductType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TestProducts(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(user=self.user, is_active=True)
        self.product_type = ProductType.objects.create(name="outdoors")


    def test_post_product(self):

        new_product = {
            "name": "cup",
            "customer": self.customer,
            "price": 17.11,
            "description": "a long string with a beautiful description",
            "quantity": 7,
            "location": "somewhere",
            "image_path": "picture.jpg",
            "created_at": "2020-02-21",
            "product_type_id": self.product_type.id 

        }

        response = self.client.post(
            reverse('product-list'), new_product, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Product.objects.count(), 1)

        self.assertEqual(Product.objects.get().name, 'cup')


    def test_get_product(self):

        new_product = Product.objects.create(
            name= "cup",
            customer= self.customer,
            price= 17.11,
            description= "a long string with a beautiful description",
            quantity= 7,
            location= "somewhere",
            image_path= "picture.jpg",
            created_at= "2020-02-21",
            product_type= self.product_type
        )

        response = self.client.get(reverse('product-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))


        self.assertEqual(response.status_code, 200)


        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["name"], "cup")


        self.assertIn(new_product.name.encode(), response.content)



    def test_delete_product(self):

        new_product = {
            "name": "cup",
            "customer": self.customer,
            "price": 17.11,
            "description": "a long string with a beautiful description",
            "quantity": 7,
            "location": "somewhere",
            "image_path": "picture.jpg",
            "created_at": "2020-02-21",
            "product_type_id": self.product_type.id 

        }

        
        response = self.client.delete(reverse('product-list')+f'/{str(self.new_product.id)}', HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 204)


        self.assertEqual(len(response.data), 0)


if __name__ == '__main__':
    unittest.main()





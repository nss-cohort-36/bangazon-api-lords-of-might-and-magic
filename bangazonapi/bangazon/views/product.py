"""Products for Bangazon"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
import sqlite3
from ..connection import Connection
from bangazon.models import Product, OrderProduct, Order


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Products

    Arguments:
        serializers
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'customer_id', 'price', 'description', 'quantity', 'location', 'image_path', 'product_type_id', 'inventory')

class Products(ViewSet):
    """Products for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Products instance
        """
        newproduct = Product()
        newproduct.name = request.data["name"]
        newproduct.customer_id = request.auth.user.customer.id
        newproduct.price = request.data["price"]
        newproduct.description = request.data["description"]
        newproduct.quantity = request.data["quantity"]
        newproduct.location = request.data["location"]
        newproduct.image_path = request.data["image_path"]
        newproduct.product_type_id = request.data["product_type_id"]
        newproduct.save()

        serializer = ProductSerializer(newproduct, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product

        Returns:
            Response -- JSON serialized product instance
        """
        if pk == '0':
            products = Product.objects.filter(customer_id=request.auth.user.customer.id)
            
            with sqlite3.connect(Connection.db_path) as conn:
                conn.row_factory = sqlite3.Row
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    SELECT p.id as product_id, COUNT(op.id) as quantity_sold
                    FROM bangazon_orderproduct op 
                    JOIN bangazon_product p
                    ON op.product_id = p.id
                    LEFT JOIN bangazon_order o
                    ON op.order_id =o.id
                    GROUP BY p.id;      
                """)

                inventory = {}
                dataset = db_cursor.fetchall()

                for row in dataset:
                    inventory[row['product_id']] = row['quantity_sold']

                for product in products:
                    if product.id in inventory:
                        product.inventory = product.quantity - inventory[product.id]
                    else: 
                        product.inventory = product.quantity
            serializer = ProductSerializer(
            products, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            try:
                product = Product.objects.get(pk=pk)
                serializer = ProductSerializer(product, context={'request': request})
                return Response(serializer.data)
            except Exception as ex:
                return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a product

        Returns:
            Response -- Empty body with 204 status code
        """
        product = Product.objects.get(pk=pk)
        product.name = request.data["name"]
        product.customer_id = request.data["customer_id"]
        product.price = request.data["price"]
        product.description = request.data["description"]
        product.quantity = request.data["quantity"]
        product.location = request.data["location"]
        product.image_path = request.data["image_path"]
        product.product_type_id = request.data["product_type_id"]
        product.save()
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to products resource

        Returns:
            Response -- JSON serialized list of products
        """
        products = Product.objects.all()
        for product in products:
            completedOrders = Order.objects.filter(payment_type__isnull=False)
            product_inventory = completedOrders.filter(pk=product.id).count()
            product.inventory = product.quantity - product_inventory
            
        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)


    # @action(methods=['get'], detail=False)
    # def my_products(self, request):
    #     current_user = Customer.objects.get(user=request.auth.user)

    #     try:
    #         product = Product.objects.filter(customer_id=current_user.id)
    #     except product.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = ProductSerializer(product, many=True, context={'request': request})
    #     return Response(serializer.data)
            

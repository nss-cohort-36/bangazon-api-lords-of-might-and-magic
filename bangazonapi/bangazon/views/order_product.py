from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazon.models import OrderProduct, Order, Product, Customer

# for custom sql method
import sqlite3
from django.shortcuts import render
# from .connection import Connection


class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for OrderProducts

    Arguments:
        serializers
    """
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'order', 'product')
        depth = 2


class OrderProducts(ViewSet):
    """Products for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Orders instance
        """
        new_order_product = OrderProduct()
        new_order_product.order_id = request.data['order_id']
        new_order_product.product_id = request.data['product_id']
        

        new_order_product.save()

        serializer = OrderProductSerializer(new_order_product, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order_product

        Returns:
            Response -- JSON serialized order_product instance
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(
                order_product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Order

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order_product_to_delete = OrderProduct.objects.get(pk=pk)
            order_product_to_delete.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to order_products resource

        Returns:
            Response -- JSON serialized list of order_products
        """
        current_user = Customer.objects.get(user=request.auth.user)

        try:
            # order_products = OrderProduct.objects.all()
            # serializer = OrderProductSerializer(
            #     order_products, many=True, context={'request': request})
            # return Response(serializer.data)

            open_order = Order.objects.get(customer=current_user, payment_type=None)
            order_products = OrderProduct.objects.filter(order=open_order)
            serializer = OrderProductSerializer(
                order_products, many=True, context={'request': request})
            return Response(serializer.data)
        except OrderProduct.DoesNotExist as ex:
            return Response([])
        except Order.DoesNotExist as ex: 
            return Response([])

    # def list(self, request):
    #     if request.method == 'GET':
    #         with sqlite3.connect(Connection.db_path) as conn:
    #             conn.row_factory = sqlite3.Row
    #             db_cursor = conn.cursor()

    #             db_cursor.execute("""
    #             SELECT
    #                 bo.id,
    #                 bo.order_id,
    #                 bo2.created_at,
    #                 bo2.customer_id,
    #                 bo2.payment_type_id,
    #                 bo.product_id,
    #                 bp.name,
    #                 bp.price,
    #                 bp.description,
    #                 bp.quantity,
    #                 bp.location,
    #                 bp.image_path,
    #                 bp.customer_id AS 'product_customer_id',
    #                 bp.product_type_id
    #             FROM bangazon_orderproduct bo
    #             JOIN bangazon_order bo2, bangazon_product bp
    #             ON bo.order_id = bo2.id
    #             AND bo.product_id = bp.id
    #             WHERE bo2.payment_type_id IS NULL
    #             AND bo2.customer_id = ?;
    #             """,
    #             (request.auth.user.customer.id,))

    #             all_books = []
    #             dataset = db_cursor.fetchall()

    #             for row in dataset:
    #                 order_product = OrderProduct()
    #                 order_product.id = row['id']
                    
    #                 order = Order()
    #                 order.id = row['order_id']
    #                 order.created_at = row['created_at']
    #                 order.customer_id = row['customer_id']
    #                 order.payment_type_id = row['payment_type_id']
                    
    #                 order_product.order = order

    #                 product = Product()
    #                 product.id = row['product_id']
    #                 product.name = row['name']
    #                 product.price = row['price']
    #                 product.description = row['description']
    #                 product.quantity = row['quantity']
    #                 product.location = row['location']
    #                 product.image_path = row['image_path']
    #                 product.customer_id = row['product_customer_id']
    #                 product.product_type_id = ['product_type_id']
                    
    #                 order_product.product = product

    #                 all_order_products = []
    #                 all_order_products.append(order_product)

    #         try:
    #             serializer = OrderProductSerializer(
    #                 all_order_products, many=True, context={'request': request})
    #             return Response(serializer.data)
    #         except Exception as ex:
    #             return HttpResponseServerError(ex)

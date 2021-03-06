"""Orders for Bangazon"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazon.models import Order
import datetime
from rest_framework.decorators import action
from .product import ProductSerializer
from .product import Product

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Orders

    Arguments:
        serializers
    """
    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'created_at', 'payment_type_id', 'products')
        

class Orders(ViewSet):
    """Orders for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Orders instance
        """
        neworder = Order()
        neworder.customer_id = request.auth.user.customer.id

        neworder.save()

        serializer = OrderSerializer(neworder, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Order

        Returns:
            Response -- JSON serialized Order instance
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a Order

        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        
        order.payment_type_id = request.data["payment_type_id"]
       

        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single Order

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order_to_delete = Order.objects.get(pk=pk)
            order_to_delete.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to Orders resource

        Returns:
            Response -- JSON serialized list of Orders
        """
        try:
            order = Order.objects.get(customer_id=request.auth.user.customer.id, payment_type = None)
            
        except Order.DoesNotExist:
            neworder = Order()
            neworder.customer_id = request.auth.user.customer.id

            neworder.save()
            order = Order.objects.get(customer_id=request.auth.user.customer.id, payment_type = None)

        serializer = OrderSerializer(
                order, context={'request': request})
        return Response(serializer.data)

    # Example request:
    #   http://localhost:8000/orders/cart
    # @action(methods=['get'], detail=False)
    # def cart(self, request):
    #     current_user = Customer.objects.get(user=request.auth.user)
    
    #     try:
    #         open_order = Order.objects.get(customer=current_user, payment_type=None)
    #         orderproducts.filter(order__id=open_order.id)
    #         products_on_order = Product.objects.filter(cart__order=open_order)
    #     except Order.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = OrderSerializer(open_order, context={'request': request})
    #     return Response(serializer.data)
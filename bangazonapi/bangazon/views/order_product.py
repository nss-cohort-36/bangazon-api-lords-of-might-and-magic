from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazon.models import OrderProduct, Order, Customer

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

class OrderProducts(ViewSet):
    """Products for Bangazon"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order_product

        Returns:
            Response -- JSON serialized order_product instance
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            serializer = OrderProductSerializer(order_product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to order_products resource

        Returns:
            Response -- JSON serialized list of order_products
        """
        for key in request:
            print('key: ', key)
        # current_user = Customer.objects.get(user_id=request.auth.user.id)

        try:
            open_order = Order.objects.get(customer_id=2, payment_type=None)

            # open_order = Order.objects.get(customer=current_user, payment_type=None)
            filtered_order_products = OrderProduct.objects.filter(order_id=open_order.id)
        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        # order_products = OrderProduct.objects.all()
        serializer = OrderProductSerializer(
            filtered_order_products, many=True, context={'request': request})
        return Response(serializer.data)
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazon.models import Customer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Customers

    Arguments:
        serializers
    """
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'is_active', 'user_id')

class Customers(ViewSet):
    """Customers for Bangazon"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single customer

        Returns:
            Response -- JSON serialized customer instance
        """
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to products resource

        Returns:
            Response -- JSON serialized list of products
        """
        customers = Customer.objects.all()
        serializer = CustomerSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)
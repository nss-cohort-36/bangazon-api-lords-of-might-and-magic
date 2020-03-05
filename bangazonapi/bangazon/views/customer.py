from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazon.models import Customer
from django.contrib.auth.models import User


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Customers

    Arguments:
        serializers
    """
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customers',
            lookup_field='id'
        )
        fields = ('id', 'url', 'user_id','user', 'address', 'city', 'phone')
        depth = 2

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
        """Handle GET requests to customer resource

        Returns:
            Response -- JSON serialized list of products
        """
        customers = Customer.objects.filter(id = request.auth.user.customer.id)
        serializer = CustomerSerializer(
            customers, many=True, context={'request': request})
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """Handle PATCH request for single customer

        Returns:
            Response -- JSON serialized customer edits
        """
        try:
            customer = Customer.objects.get(pk = pk)
            customer.phone = request.data["phone"]
            customer.address = request.data["address"]
            customer.city = request.data["city"]
            customer.save()

            user = User.objects.get(pk=pk)
            user.last_name = request.data["last_name"]
            user.save()
        
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Exception as ex:
            return HttpResponseServerError(ex)

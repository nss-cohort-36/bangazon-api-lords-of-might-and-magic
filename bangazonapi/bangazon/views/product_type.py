"""Products for Bangazon"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazon.models import ProductType


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for ProductTypes

    Arguments:
        serializers
    """
    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='producttype',
            lookup_field='id'
        )
        fields = ('id', 'name')
        

class ProductTypes(ViewSet):
    """Products for Bangazon"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product type

        Returns:
            Response -- JSON serialized product type instance
        """
        try:
            product_type = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(product_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to products resource

        Returns:
            Response -- JSON serialized list of products
        """
        product_types = ProductType.objects.all()
        serializer = ProductTypeSerializer(
            product_types, many=True, context={'request': request})
        return Response(serializer.data)
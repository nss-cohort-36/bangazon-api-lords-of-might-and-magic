"""Product Types for Bangazon"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from bangazon.models import ProductType


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Product Types

    Arguments:
        serializers
    """
    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='product_type',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', )

class ProductTypes(ViewSet):
    """Product types for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Products instance
        """
        new_product_type = ProductType()
        new_product_type.name = request.data["name"]
        new_product_type.save()

        serializer = ProductTypeSerializer(new_product_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product type

        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product_type = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(product_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    # def update(self, request, pk=None):
    #     """Handle PUT requests for a product

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     product_type = Product()
    #     product_type.name = request.data["name"]
    #     product_type.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product_type = ProductType.objects.get(pk=pk)
            product_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProductType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to product types resource

        Returns:
            Response -- JSON serialized list of product types
        """
        product_type = ProductType.objects.all()
        serializer = ProductTypeSerializer(
            product_type, many=True, context={'request': request})
        return Response(serializer.data)


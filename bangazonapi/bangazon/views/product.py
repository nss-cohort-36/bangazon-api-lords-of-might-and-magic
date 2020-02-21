"""Products for Bangazon"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazon.models import Product

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
        fields = ('id', 'url', 'name', 'customerId', 'price', 'description', 'quantity', 'location', 'imagePath', 'createdAt', 'productTypeId')

class Products(ViewSet):
    """Products for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Products instance
        """
        newproduct = Product()
        newproduct.name = request.data["name"]
        newproduct.customerId = request.data["customerId"]
        newproduct.price = request.data["price"]
        newproduct.description = request.data["description"]
        newproduct.quantity = request.data["quantity"]
        newproduct.location = request.data["location"]
        newproduct.imagePath = request.data["imagePath"]
        newproduct.createdAt = request.data["createdAt"]
        newproduct.productTypeId = request.data["productTypeId"]
        newproduct.save()

        serializer = ProductSerializer(newproduct, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product

        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    # def update(self, request, pk=None):
    #     """Handle PUT requests for a product

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """
    #     product = Product()
    #     product.name = request.data["name"]
    #     product.customerId = request.data["customerId"]
    #     product.price = request.data["price"]
    #     product.description = request.data["description"]
    #     product.quantity = request.data["quantity"]
    #     product.location = request.data["location"]
    #     product.imagePath = request.data["imagePath"]
    #     product.createdAt = request.data["createdAt"]
    #     product.productTypeId = request.data["productTypeId"]
    #     product.save()

    #     return Response({}, status=status.HTTP_204_NO_CONTENT)

    # def destroy(self, request, pk=None):
    #     """Handle DELETE requests for a single product

    #     Returns:
    #         Response -- 200, 404, or 500 status code
    #     """
    #     try:
    #         product = Product.objects.get(pk=pk)
    #         product.delete()

    #         return Response({}, status=status.HTTP_204_NO_CONTENT)

    #     except Product.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to products resource

        Returns:
            Response -- JSON serialized list of products
        """
        products = Product.objects.all()
        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

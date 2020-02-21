"""Payment Types for Bangazon"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazon.models import PaymentType

class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Payment Types

    Arguments:
        serializers
    """
    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymentType',
            lookup_field='id'
        )
        fields = ('id', 'url', )

class PaymentTypes(ViewSet):
    """Payment Types for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Payment Types instance
        """
        newpaymentType = PaymentType()
        newpaymentType.merchant_name = request.data["merchant_name"]
        newpaymentType.acct_number = request.data["acct_number"]
        newpaymentType.expiration_date = request.data["expiration_date"]
        newpaymentType.customerId = request.data["customerId"]
        newpaymentType.created_at = request.data["created_at"]

        newpaymentType.save()

        serializer = PaymentTypeSerializer(newpaymentType, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Payment Type

        Returns:
            Response -- JSON serialized Payment Type instance
        """
        try:
            paymentType = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(paymentType, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a Payment Type

        Returns:
            Response -- Empty body with 204 status code
        """
        newpaymentType = PaymentType()
        newpaymentType.merchant_name = request.data["merchant_name"]
        newpaymentType.acct_number = request.data["acct_number"]
        newpaymentType.expiration_date = request.data["expiration_date"]
        newpaymentType.customerId = request.data["customerId"]
        newpaymentType.created_at = request.data["created_at"]

        newpaymentType.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single payment type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            PaymentType = PaymentType.objects.get(pk=pk)
            PaymentType.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to payment types resource

        Returns:
            Response -- JSON serialized list of payment types
        """
        paymentTypes = PaymentType.objects.all()
        serializer = PaymentTypeSerializer(
            paymentTypes, many=True, context={'request': request})
        return Response(serializer.data)


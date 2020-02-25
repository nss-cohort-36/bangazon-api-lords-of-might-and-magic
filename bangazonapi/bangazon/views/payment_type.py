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
            view_name='paymenttype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'merchant_name', 'acct_number', 'expiration_date', 'created_at')

class PaymentTypes(ViewSet):
    """Payment Types for Bangazon"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Payment Types instance
        """
        new_payment_type = PaymentType()
        new_payment_type.merchant_name = request.data["merchant_name"]
        new_payment_type.acct_number = request.data["acct_number"]
        new_payment_type.expiration_date = request.data["expiration_date"]
        new_payment_type.customer_id = request.auth.user.customer.id

        new_payment_type.save()

        serializer = PaymentTypeSerializer(new_payment_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single Payment Type

        Returns:
            Response -- JSON serialized Payment Type instance
        """
        try:
            payment_type = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(payment_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a Payment Type

        Returns:
            Response -- Empty body with 204 status code
        """
        new_payment_type = PaymentType()
        new_payment_type.merchant_name = request.data["merchant_name"]
        new_payment_type.acct_number = request.data["acct_number"]
        new_payment_type.expiration_date = request.data["expiration_date"]
        new_payment_type.customer_id = request.auth.user.customer.id
        new_payment_type.created_at = request.data["created_at"]

        new_payment_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single payment type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            payment_type = PaymentType.objects.get(pk=pk)
            payment_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, pk=None):
        """Handle GET requests to payment types of current user

        Returns:
            Response -- JSON serialized list of payment types
        """
        payment_types = PaymentType.objects.filter(customer_id=request.auth.user.customer.id)
        serializer = PaymentTypeSerializer(
            payment_types, many=True, context={'request': request})
        return Response(serializer.data)

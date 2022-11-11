from rest_framework import serializers
from .models import User, Delivery, Prescription, Welfare

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "user_type",
            "email",
            "phone_number",
            "address_1",
            "address_2",
            "city",
            "postcode",
        )

class deliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = (
            "order",
            "date_created",
            "date_due",
            "status",
            "operator"
        )

class prescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = (
            "order_details",
            "pharmacy",
            "date_created",
            "date_due",
            "status",
            "operator"
        )

class welfareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Welfare
        fields = (
            "notes",
            "date_created",
            "date_due",
            "status",
            "operator"
        )
from django.utils import timezone as tz

from rest_framework import serializers

from tracksales.sales.models import Client, Employee


class MonthYearSerializer(serializers.Serializer):
    month = serializers.IntegerField(required=False)
    year = serializers.IntegerField(default=tz.now().year)

    def validate_month(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError("Month must be between 1 and 12.")
        return value

    def validate_year(self, value):
        if value < 2000 or value > 2100:
            raise serializers.ValidationError("Year must be between 2000 and 2100.")
        return value
    

class EmployeeStatisticSerializer(serializers.ModelSerializer):
    total_clients = serializers.IntegerField(default=0)
    total_products = serializers.IntegerField(default=0)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if not representation['total_products']:
            representation['total_products'] = 0

        if not representation['total_amount']:
            representation['total_amount'] = '0.00'

        return representation

    class Meta:
        model = Employee
        fields = ('id', 'full_name', 'total_clients', 'total_products', 'total_amount')


class ClientStatisticSerializer(serializers.ModelSerializer):
    total_products = serializers.IntegerField(default=0)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if not representation['total_products']:
            representation['total_products'] = 0

        if not representation['total_amount']:
            representation['total_amount'] = '0.00'

        return representation

    class Meta:
        model = Client
        fields = ('id', 'full_name', 'total_products', 'total_amount')


class EmployeesStatisticSerializer(serializers.ModelSerializer):
    total_clients = serializers.IntegerField(default=0)
    total_products = serializers.IntegerField(default=0)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if not representation['total_products']:
            representation['total_products'] = 0

        if not representation['total_amount']:
            representation['total_amount'] = '0.00'

        return representation

    class Meta:
        model = Employee
        fields = ('id', 'full_name', 'total_clients', 'total_products', 'total_amount')
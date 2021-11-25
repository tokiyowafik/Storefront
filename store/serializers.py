from rest_framework import serializers
from decimal import Decimal

from rest_framework.relations import HyperlinkedRelatedField
from .models import Product, Collection

# A serializer is an object that takes an object and converts it to a python dictionary
# A serializer also can take a queryset but 'many' argument has to be set to True
# To create a custom field in serializer that doesn't exist in actual obj, user SerializerMethodField class (method name must start with get)
# To rename the serializer field, 'source' argument must be filled with the actual name of the field
# Use Model Serializer to get rid of all repetitions in the serializer classes
# To override is_valid() method, validate method should take 2 arguments, self and data(dict), and either returns validation error or the actual data(dict)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField()

    def get_price_with_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    #example
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match.')
    #     return data

    #example
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product

    #example
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance

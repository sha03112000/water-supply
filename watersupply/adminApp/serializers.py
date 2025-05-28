from rest_framework import serializers
from django.contrib.auth import get_user_model
from . models import Products, Orders

class ProductSerializer(serializers.ModelSerializer):
    is_available = serializers.BooleanField(default=True, read_only=True)
    
    class Meta:
        model = Products
        fields = '__all__'
        
    
    def validate(self, data):
        product_price = data.get('product_price')
        product_rate = data.get('product_rate')
        
        if product_rate > product_price:
            raise serializers.ValidationError({
                'product_price': "Product price must be greater than product rate."
            })

        return data
        
    
    def create(self, validated_data):
        product_image = validated_data.pop('product_image', None)
        products = Products.objects.create(**validated_data)
        if product_image:
            products.product_image = product_image
            products.save()
        return products
    

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
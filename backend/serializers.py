from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import Shop, User, ProductInfo, Product, Category, Order


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'user_type', 'groups', ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name', ]


class ShopSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Shop
        fields = ['id', 'name', 'url', 'user', ]


class ShopShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['category', 'name', ]


class ProductInfoSerializer(serializers.ModelSerializer):
    shop = ShopShortSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductInfo
        fields = ['shop', 'product', 'quantity', 'price', 'price_rrc']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['user', 'dt', 'status', ]

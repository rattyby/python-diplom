from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Shop, User, ProductInfo, Product, Category, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'user_type', 'groups', ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_staff', 'user_type', 'groups', ]
        extra_kwargs = {'first_name': {'required': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


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
        fields = ['id', 'shop', 'product', 'quantity', 'price', 'price_rrc']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductInfoSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', ]


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    address = serializers.CharField(required=True)
    status = serializers.CharField(required=True)
    products = OrderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Order
        fields = ['user', 'dt', 'address', 'status', 'products', ]


class ProductAddSerializer(serializers.ModelSerializer):
    product = ProductInfoSerializer(read_only=True)
    quantity = serializers.IntegerField(required=True, validators=[])

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', ]

    def validate(self, data):
        """
        Количество в заказе не должно превышать наличие в магазине.
        Still not works.
        """
        try:
            product = ProductInfo.objects.get(id=data['product'])
        except ObjectDoesNotExist as e:
            raise ValidationError('Not found such product.')
        max_count = product['quantity']
        if data['quantity'] > max_count:
            raise ValidationError('Not enough items in the shop.')
        return data

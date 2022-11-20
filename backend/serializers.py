from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import Shop, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'user_type', 'groups', ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'url', ]

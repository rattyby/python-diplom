from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PriceUpdate(APIView):
    """
    Обновление прайса для магазина.
    """
    def post(self, request, *args, **kwargs):
        data = request.data.get('url')
        return JsonResponse({'Status': True, 'method': 'post', 'data': data})

    def get(self, request, *args, **kwargs):
        return JsonResponse({'Status': True, 'method': 'get'})

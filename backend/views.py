from django.contrib.auth.models import Group
from django.core.validators import URLValidator
from django.http import JsonResponse
from requests import get
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from yaml import Loader, load as load_yaml

from .models import User, ProductInfo, Shop, Category, Product, Parameter, ProductParameter

from .serializers import UserSerializer, GroupSerializer, ShopSerializer, ProductInfoSerializer


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
        if not request.user.is_authenticated:
            return JsonResponse({'Status': status.HTTP_403_FORBIDDEN, 'Error': 'Log in required.'})
        if not request.user.user_type == 'shop':
            return JsonResponse({'Status': status.HTTP_403_FORBIDDEN, 'Error': 'Only shops can do that.'})

        # Получаем ссылку на файл.
        url = request.data.get('url')

        if url:
            validate_url = URLValidator()
            try:
                validate_url(url)
            except ValidationError as e:
                return JsonResponse({'Stasus': status.HTTP_400_BAD_REQUEST, 'Error': str(e)})

            # Читаем файл.
            stream = get(url).content
            data = load_yaml(stream, Loader=Loader)

            # Заполняем таблицы из полученного файла.
            user = User.objects.get(id=request.user.id)
            shop, _ = Shop.objects.get_or_create(name=data['shop'], id_user=user)
            for category in data['categories']:
                category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                category_object.shops.add(shop.id)
                category_object.save()
            ProductInfo.objects.filter(shop=shop.id).delete()
            for item in data['goods']:
                category = Category.objects.get(id=item['category'])
                product, _ = Product.objects.get_or_create(category=category, name=item['name'])

                product_info, _ = ProductInfo.objects.get_or_create(product=product,
                                                                    shop=shop,
                                                                    external_id=item['id'],
                                                                    model=item['model'],
                                                                    price=item['price'],
                                                                    price_rrc=item['price_rrc'],
                                                                    quantity=item['quantity'])
                for name, value in item['parameters'].items():
                    parameter_object, _ = Parameter.objects.get_or_create(name=name)
                    ProductParameter.objects.create(product_info=product_info,
                                                    parameter=parameter_object,
                                                    value=value)
            return JsonResponse({'Status': status.HTTP_201_CREATED, 'data': request.data})
        return JsonResponse({'Status': status.HTTP_400_BAD_REQUEST, 'Error': 'No URL with your price.'})

    def get(self, request, *args, **kwargs):
        catalog = ProductInfo.objects.all()
        serializer = ProductInfoSerializer(catalog, many=True)
        return JsonResponse({'Status': status.HTTP_200_OK, 'method': 'get'})

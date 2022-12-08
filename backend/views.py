from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import URLValidator
from django.http import JsonResponse
from requests import get
from rest_framework import viewsets, permissions, status, generics, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from yaml import Loader, load as load_yaml

from .models import User, ProductInfo, Shop, Category, Product, Parameter, ProductParameter, Order, OrderItem

from .serializers import UserSerializer, GroupSerializer, ShopSerializer, ProductInfoSerializer, OrderSerializer, \
    RegisterSerializer, ProductAddSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RegisterUserView(generics.CreateAPIView):
    """
    Регистрация пользователя.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PriceUpdateView(APIView):
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
                return JsonResponse({'Status': status.HTTP_400_BAD_REQUEST, 'Error': str(e)})

            # Читаем файл.
            stream = get(url).content
            data = load_yaml(stream, Loader=Loader)

            # Заполняем таблицы из полученного файла.
            try:
                user = User.objects.get(id=request.user.id)
            except ObjectDoesNotExist as e:
                JsonResponse({'Status': status.HTTP_404_NOT_FOUND, 'Error': str(e)})

            # Shop model.
            shop, _ = Shop.objects.get_or_create(name=data['shop'], id_user=user)

            for category in data['categories']:
                # Category model.
                category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                category_object.shops.add(shop.id)
                category_object.save()

            ProductInfo.objects.filter(shop=shop.id).delete()
            for item in data['goods']:
                try:
                    category = Category.objects.get(id=item['category'])
                except ObjectDoesNotExist as e:
                    JsonResponse({'Status': status.HTTP_404_NOT_FOUND, 'Error': str(e)})

                # Product model.
                product, _ = Product.objects.get_or_create(category=category, name=item['name'])

                # ProductInfo model.
                product_info, _ = ProductInfo.objects.get_or_create(product=product,
                                                                    shop=shop,
                                                                    external_id=item['id'],
                                                                    model=item['model'],
                                                                    price=item['price'],
                                                                    price_rrc=item['price_rrc'],
                                                                    quantity=item['quantity'])

                for name, value in item['parameters'].items():
                    # Parameter model.
                    parameter_object, _ = Parameter.objects.get_or_create(name=name)

                    # ProductParameter model.
                    ProductParameter.objects.create(product_info=product_info,
                                                    parameter=parameter_object,
                                                    value=value)
            return JsonResponse({'Status': status.HTTP_201_CREATED, 'data': request.data})
        # No 'url' field.
        return JsonResponse({'Status': status.HTTP_400_BAD_REQUEST, 'Error': 'No URL with your price.'})

    def get(self, request, *args, **kwargs):
        catalog = ProductInfo.objects.all()
        serializer = ProductInfoSerializer(catalog, many=True)
        return JsonResponse({'Status': status.HTTP_200_OK, 'method': 'get'})


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductAddView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = ProductAddSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Добавление товара в корзину. Если у пользователя есть заказ со статусом 'basket', то добавляется к нему,
        иначе создаётся новый.
        В параметрах запроса надо передавать id продукта из ProductInfo.
        """
        if not request.user.is_authenticated:
            return JsonResponse({'Status': status.HTTP_403_FORBIDDEN, 'Error': 'Log in required.'})

        try:
            user = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist as e:
            JsonResponse({'Status': status.HTTP_404_NOT_FOUND, 'Error': str(e)})

        order, _ = Order.objects.get_or_create(user=user, status='basket')
        try:
            product = ProductInfo.objects.get(id=request.data['product'])
        except ObjectDoesNotExist as e:
            JsonResponse({'Status': status.HTTP_404_NOT_FOUND, 'Error': str(e)})
        add_item, _ = OrderItem.objects.get_or_create(order=order,
                                                      product=product,
                                                      shop=product.shop,
                                                      quantity=request.data['quantity'])

        return JsonResponse({'Status': status.HTTP_201_CREATED, 'data': request.data})


class ConfirmOrderView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': status.HTTP_403_FORBIDDEN, 'Error': 'Log in required.'})

        try:
            user = User.objects.get(id=request.user.id)
        except ObjectDoesNotExist as e:
            JsonResponse({'Status': status.HTTP_404_NOT_FOUND, 'Error': str(e)})
        try:
            order = Order.objects.get(user=user, status='basket')
        except ObjectDoesNotExist as e:
            JsonResponse({'Status': status.HTTP_404_NOT_FOUND, 'Error': str(e)})
        order.status = 'accepted'
        order.save()
        return JsonResponse({'Status': status.HTTP_201_CREATED, 'data': request.data})

from django.contrib.auth.models import AbstractUser
from django.db import models

# Типы пользователей.
USER_TYPE_CHOICES = (
    ('shop', 'Магазин'),
    ('buyer', 'Покупатель'),
)
# Статусы заказа.
ORDER_STATUS_CHOICES = (
    ('basket', 'В корзине'),
    ('accepted', 'Принят'),
    ('payed', 'Оплачен'),
    ('posted', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('returned', 'Возвращён'),
    ('cancelled', 'Отменён'),
    ('filling', 'Собирается'),
)


class User(AbstractUser):
    """ Модификация стандартного пользователя. """
    user_type = models.CharField(verbose_name='Тип пользователя',
                                 choices=USER_TYPE_CHOICES,
                                 max_length=5,
                                 default='buyer')


class Shop(models.Model):
    """ Магазин. Связан с пользователем. """
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка')
    # filename


class Category(models.Model):
    """ Категория товаров. """
    id = models.PositiveIntegerField(primary_key=True)
    shops = models.ManyToManyField(Shop, verbose_name='Магазин')
    name = models.CharField(max_length=120, verbose_name='Название')


class Product(models.Model):
    """ Товар. Относится к одной категории. """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=120, verbose_name='Наименование')


class ProductInfo(models.Model):
    """ Наличие и цена товаров в различных магазинах. """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='goods')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин', related_name='goods')
    external_id = models.PositiveIntegerField(verbose_name='ext ID')
    model = models.CharField(max_length=150, verbose_name='Модель')
    name = models.CharField(max_length=300, verbose_name='Описание')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')


class Parameter(models.Model):
    """ Параметр товара. """
    name = models.CharField(max_length=50, verbose_name='Параметр')


class ProductParameter(models.Model):
    """ Значения параметров у конкретного товара. """
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, verbose_name='Информация')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name='Параметр')
    value = models.CharField(max_length=300, verbose_name='Значение')


class Order(models.Model):
    """ Заказ конкретного пользователя. """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Заказчик')
    dt = models.DateTimeField(verbose_name='Дата заказа', auto_now=True)
    status = models.CharField(max_length=9, choices=ORDER_STATUS_CHOICES)


class OrderItem(models.Model):
    """ Товары в заказе. """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='products')
    product = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, verbose_name='Товар', related_name='products')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    quantity = models.PositiveIntegerField(verbose_name='Количество')


class Contact(models.Model):
    """ Контакты пользователя. """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Заказчик')
    type = models.CharField(max_length=40, verbose_name='Канал связи')
    value = models.CharField(max_length=300, verbose_name='Значение')

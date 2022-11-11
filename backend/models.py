from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Shop(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField(verbose_name='URL')
    # filename


class Category(models.Model):
    shops = models.ManyToManyField(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    name = models.CharField(max_length=120, verbose_name='Название')


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=120, verbose_name='Наименование')


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    name = models.CharField(max_length=300, verbose_name='Описание')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')


class Parameter(models.Model):
    name = models.CharField(max_length=50, verbose_name='Параметр')


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE, verbose_name='Информация')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name='Параметр')
    value = models.CharField(max_length=300, verbose_name='Значение')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Заказчик')
    dt = models.DateTimeField(verbose_name='Дата заказа', auto_now=True)
    status = models.CharField(max_length=40)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    quantity = models.PositiveIntegerField(verbose_name='Количество')


class Contact(models.Model):
    type = models.CharField(max_length=40, verbose_name='Канал связи')
    user = models.ForeignKey(User, verbose_name='Заказчик')
    value = models.CharField(max_length=300, verbose_name='Значение')

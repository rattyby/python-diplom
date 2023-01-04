from django.urls import path, include
from rest_framework import routers

from .views import PriceUpdateView, UserViewSet, GroupViewSet, RegisterUserView, CatalogViewSet, OrderViewSet,\
    ProductAddView, ConfirmOrderView

app_name = 'backend'

# Routers
router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('group', GroupViewSet)
router.register('product', CatalogViewSet, basename='product')
router.register('order', OrderViewSet)

urlpatterns = [
    path('partner/update/', PriceUpdateView.as_view(), name='price-update'),
    path('user/register/', RegisterUserView.as_view(), name='user-register'),
    path('order/create/', ProductAddView.as_view(), name='create-order'),
    path('order/confirm/', ConfirmOrderView.as_view(), name='confirm-order'),
    path('', include(router.urls)),
]

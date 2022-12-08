from django.urls import path, include
from rest_framework import routers

from .views import PriceUpdateView, UserViewSet, GroupViewSet, RegisterUserView, CatalogViewSet, OrderViewSet,\
    ProductAddView, ConfirmOrderView

app_name = 'backend'

# Routers
router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('group', GroupViewSet)
router.register('product', CatalogViewSet)
router.register('order', OrderViewSet)

urlpatterns = [
    path('partner/update/', PriceUpdateView.as_view(), name='price-update'),
    path('user/register/', RegisterUserView.as_view(), name='user-register'),
    path('order/create/', ProductAddView.as_view(), name='create-order'),
    path('order/confirm/', ConfirmOrderView.as_view(), name='confirm-order'),
    # path('products', CatalogView.as_view(), name='catalog'),
    path('', include(router.urls)),
    # path('partner/state', PartnerState.as_view(), name='partner-state'),
    # path('user/register/confirm', ConfirmAccount.as_view(), name='user-register-confirm'),
    # path('user/<int:pk>', UserViewSet.as_view(), name='user-details'),
    # path('user/contact', ContactView.as_view(), name='user-contact'),
    # path('user/login', LoginAccount.as_view(), name='user-login'),
    # path('user/password_reset', reset_password_request_token, name='password-reset'),
    # path('user/password_reset/confirm', reset_password_confirm, name='password-reset-confirm'),
    # path('categories', CategoryView.as_view(), name='categories'),
    # path('shops', ShopView.as_view(), name='shops'),
    # path('basket', BasketView.as_view(), name='basket'),
    # path('order', OrderView.as_view(), name='order'),
]

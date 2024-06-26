from django.contrib import admin
from django.urls import path

from .views import *


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('signin/',login_user,name="login_user"),
    path('cart/',cart,name='cart'),
    path('updateItem/',updateItem,name='updateItem'),
    path('register/',Register_user,name="Register"),
    path('products/',products,name="products"),
    path('add_product/',add_product,name="add_product"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

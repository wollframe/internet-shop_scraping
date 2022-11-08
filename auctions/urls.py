from django.urls import path
from .views import *

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("product/<int:g_id>/", views.product, name="product"),
    path("create/", views.create, name="create"),
    path('fill-database/', views.fill_database, name='fill_database')
]

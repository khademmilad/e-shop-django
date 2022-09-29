from django.urls import path
from .views import home
from . import views

app_name = "account"

urlpatterns = [
    path('', home, name="home"),
    path('login/', views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('<user_id>/profile/', views.profile_view, name='profile')
]
from django.urls import path
from account.views import (
home, 
login_view, 
register_view, 
logout_view, 
# profile_view,
edit_account_view,
)

app_name = "account"

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    path('logout/', logout_view, name='logout'),
    # path('<user_id>/profile/', profile_view, name='profile'),
    path('<user_id>/profile/', edit_account_view, name='profile')
]
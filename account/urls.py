from django.urls import path
from .views import Login, Logout, change_pwd, reset_password, ListUserView, add_user

app_name = 'account'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('change-password/', change_pwd, name='change-password'),
    path('reset-password/', reset_password, name='reset-password'),
    path('user/list-users/', ListUserView.as_view(), name='list-user'),
    path('user/add-user/', add_user, name='add-user'),
]

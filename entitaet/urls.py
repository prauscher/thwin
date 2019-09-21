from django.urls import path

from . import views, login

urlpatterns = [
    path('', views.index, name='index'),
    path('login/token/<str:token>', login.login_by_token, name='login_by_token'),
    path('login/request_token', login.request_token),
    path('login', login.login_by_code, name='login'),
    path('logout', login.logout, name='logout'),
]

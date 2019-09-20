from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/token/<str:token>', views.login_by_token, name='login_by_token'),
    path('login/request_token', views.request_token),
    path('login', views.login_by_code, name='login'),
    path('logout', views.logout, name='logout'),
]

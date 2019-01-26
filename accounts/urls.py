from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.Login.as_view(), name='login'),
    # path('login', views.login, name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]

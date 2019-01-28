from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500

from qaapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='accounts')),
    path('', include('qaapp.urls', namespace='qa')),
]

handler404 = views.handler404

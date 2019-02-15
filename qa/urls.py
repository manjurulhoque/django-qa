from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='accounts')),
    path('', include('qaapp.urls', namespace='qa')),

    # API
    path('api/', include('accounts.api.urls')),
    path('api/', include('qaapp.api.urls')),
]

# handler404 = views.handler404

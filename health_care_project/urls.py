 
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('predict.urls')),
    path('api/', include('predict.api.urls')),
    path('account/', include('account.urls')),
    
]

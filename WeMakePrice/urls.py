from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('string-handler/', include('string_handler.urls', namespace='string-handler')),
]

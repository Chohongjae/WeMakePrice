from django.urls import path

from . import views

app_name = 'string_handler'
urlpatterns = [
    path('', views.StringHandlerView.as_view(), name='handler'),
]

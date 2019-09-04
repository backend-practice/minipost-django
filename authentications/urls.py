from django.urls import path

from . import views

app_name = 'authentications'

urlpatterns = [
    path('', views.Authentications.as_view(), name='authentications'),
]

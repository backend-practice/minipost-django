from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.UserList.as_view(), name='list'),
    path('<int:pk>/', views.UserDetail.as_view(), name='detail'),
]

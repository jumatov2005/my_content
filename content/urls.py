from django.urls import path
from . import views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete/<int:pk>/', views.delete_content, name='delete_content'),


]


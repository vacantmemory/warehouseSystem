from django.urls import path
from . import views

urlpatterns = {
    path('graph', views.index, name='index'),
    path('search', views.search, name='search'),
}
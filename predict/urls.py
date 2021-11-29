from django.urls import path

from . import views 

app_name = "predict"
urlpatterns = [ 
    path('', views.index, name="index"),
    path('disease/<int:id>/detail', views.disease_detail, name="disease_detail"),


]
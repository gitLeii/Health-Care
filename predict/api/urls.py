from django.urls import path 

from predict.api.views import prediction 


urlpatterns = [ 
    path('predict', prediction, name="prediction"),
    
]
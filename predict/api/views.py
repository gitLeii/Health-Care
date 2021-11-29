from django.http import HttpResponse, JsonResponse
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
import io 

from .utility import make_prediction
from predict.models import Disease



# @csrf_exempt
@api_view(['POST'])
def prediction(request):
    if request.method=="POST":
        # print(request) 
        # print(type(request.data),request.data)

        # request.body
        """  byte_data = request.data 
        stream = io.BytesIO(byte_data) 
        python_data = JSONParser().parse(stream)  """
        
        python_data = request.data
        if len(python_data["data"])==0:
            msg = {"msg":"empty"}
        else: 
            prediction2 = make_prediction(python_data["data"]) 
            predicted_disease_description = list()
            for p in prediction2:
                disease = Disease.objects.get(name = p[0]) 
                predicted_disease_description.append({"id":disease.id, "name":disease.name, "description":disease.description,"percentage":p[1] }) 
            
            msg = {"msg":"success", "data": predicted_disease_description} 
        return JsonResponse(msg)
        # return Response(msg)

    
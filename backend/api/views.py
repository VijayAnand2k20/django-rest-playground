from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

@api_view(['GET'])
def api_home(request):
    '''
    DRF API View
    '''
    instance = Product.objects.all().order_by("?").first()
    data = {}
    if instance:
        # data = model_to_dict(instance, fields=["id","title", "price", "sale_price"])
        data = ProductSerializer(instance).data
    return Response(data)
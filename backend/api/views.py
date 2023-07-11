from django.http import JsonResponse
from products.models import Product
import json

def api_home(request):
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data['id'] = model_data.pk
        data['title'] = model_data.title
        data['content'] = model_data.content
        data['price'] = model_data.price
        # model instance (model_data)
        # turn into python dictionary
        # return JSON to client
    return JsonResponse(data)
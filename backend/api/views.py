from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
import json

from products.models import Product

def api_home(request):
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data = model_to_dict(model_data, fields=["id","title"])
        # json_data_string = json.dumps(data)
    # return HttpResponse(json_data_string, headers={"Content-Type": "application/json"})
    return JsonResponse(data)
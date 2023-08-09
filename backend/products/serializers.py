from rest_framework import serializers
from rest_framework.reverse import reverse

from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='products-api:detail',
        lookup_field='pk',
    )
    class Meta:
        model = Product
        fields = [
            'url',
            'edit_url',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount',
        ]
    
    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('products-api:edit', kwargs={'pk': obj.pk}, request=request)
    
    def get_my_discount(self, obj):
        # try:
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()
        # except:
        #     return None
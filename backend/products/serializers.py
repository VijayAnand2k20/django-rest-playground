from rest_framework import serializers
from rest_framework.reverse import reverse

from products.models import Product
from .validators import validate_title_no_hello, unique_product_title

class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='products-api:detail',
        lookup_field='pk',
    )
    title = serializers.CharField(validators=[validate_title_no_hello, unique_product_title])
    name = serializers.CharField(source='title', read_only=True)
    class Meta:
        model = Product
        fields = [
            'url',
            'edit_url',
            'pk',
            'name',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount',
        ]
    
    # def validate_title(self, value):
    #     request = self.context.get('request')
    #     user = request.user
    #     qs = Product.objects.filter(title__iexact=value,user=user)
    #     if qs.exists():
    #         raise serializers.ValidationError("This title is already in use")
    #     return value
    
    def create(self, validate_data):
        # return Product.objects.create(**validate_data)
        obj = super().create(validate_data)
        return obj

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

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
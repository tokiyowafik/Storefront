# Create your views here.
# Note: View function is a function that takes a request and returns a response
""" 
    api_view() decorator:
    - browasable api ui
    - change the request and response in django to request and response in restframework
"""
"""
    1. Get an obj -> Product.objects.get(pk=id)
    2. Convert the obj to python dict -> ProductSerializer(obj)
    3. Get the python dict -> serializer.data
    4. The JSONRenderer proses will happen under the hood
"""
"""
    There are four ways to serializing relationship:
        1. By its primary key
        2. By its string representation
        3. By its serializer
        4. By its url
"""
"""
    Deserializing object:
    1. Create a serializer and pass request.data as an argument (data=request.data)
    2. Validate the request data
       (We can use is_valid() method from rest_framework, but if we need anything extra we can override the validate method in the serializer class)
    3. Save the request data to the database
        - Create
            > can be override inside a serializer
            > return the object that has been created and status 201 if success
        - Update
            > pass the instance to the serializer (instance=...., data=....)
            > can be override inside a serializer
"""
"""
    Class based views:
    Using Class-based view:
        1. import APIView from rest_framework.views
        2. Change the urls
            path('.../', views.ObjectList.as_view())

    Class-based view benefits:
        1. Get rid of many nested if statements
"""

from django.db.models.fields import Field
from django.shortcuts import get_object_or_404
from django.db.models import Count, F, query
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from .models import Collection, OrderItem, Product
from .serializers import CollectionSerializer, ProductSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Collection cannot be deleted because it is associated with one or more products'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because it is associated with one or more orderitems'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer
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
            > can be override inside a serializer
"""


@api_view()
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    serializer = CollectionSerializer(collection)
    return Response(serializer.data)
    

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.shortcuts import get_object_or_404,render
from .models import Product
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response  
from .serializers import ProductSerializer
from rest_framework import status

from .filters import ProductsFilter

from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import IsAuthenticated




# Create your views here.

@api_view(['GET'])
def get_all_products(request):
    filterset = ProductsFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    count = filterset.qs.count()
    resPage = 20
    paginator = PageNumberPagination()
    paginator.page_size = resPage
    queryset = paginator.paginate_queryset(filterset.qs,request)
    serilizer = ProductSerializer(queryset,many=True)
    print(serilizer)
    return Response({"products":serilizer.data,"per_page":resPage,"count":count})


       # products = Product.objects.all()
       # print(products)
       # serilizer = ProductSerializer(products,many=True)




@api_view(['GET'])
def get_product(request,pk):
    products = get_object_or_404(Product,id=pk)
    print(products)
    serilizer = ProductSerializer(products,many=False)
    print(serilizer)
    return Response({"product":serilizer.data})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serilizer = ProductSerializer(data = data)
    
    if serilizer.is_valid():
        product = Product.objects.create(**data,user=request.user)
        result= ProductSerializer(product,many=False)
        
        return Response({"product":result.data})
    else:
        return Response(serilizer.errors)
    
    
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request,pk):
    product = get_object_or_404(Product,id=pk)
    if product.user != request.user:
        return Response({'error':'Sorry you can not update this product'},status=status.HTTP_403_FORBIDDEN)
    
    product.name = request.data['name']    
    product.description = request.data['description']    
    product.price = request.data['price']    
    product.brand = request.data['brand']    
    product.category = request.data['category']    
    product.ratings = request.data['ratings']    
    product.stock = request.data['stock']    
    
    product.save()
    serializer = ProductSerializer(product,many=False)
    return Response({"product":serializer.data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request,pk):
    product = get_object_or_404(Product,id=pk)
    if product.user != request.user:
        return Response({'error':'Sorry you can not update this product'},status=status.HTTP_403_FORBIDDEN)
    
    
    product.delete()
    return Response({"product":"Delete action is done"},status=status.HTTP_200_OK)
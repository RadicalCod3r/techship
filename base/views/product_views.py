from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status

from ..models import Product, Review
from ..serializers import ProductSerializer

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword')

    if query == None:
        query = ''

    # print(query)

    products = Product.objects.filter(name__icontains=query)

    page = request.query_params.get('page')
    paginator = Paginator(products, 5)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)

    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'pages': paginator.num_pages, 'page': page})

@api_view(['GET'])
def getTopProducts(request):
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([permissions.IsAdminUser,])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Deleted Successfully')

@api_view(['POST',])
@permission_classes([permissions.IsAdminUser,])
def createProduct(request):
    user = request.user

    product = Product.objects.create(
        user=user,
        name='Sample Name',
        brand='Sample Brand',
        category='Sample Category',
        description='',
        price=0,
        countInStock=0
    )

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser,])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)

    product.name = data['name']
    product.brand = data['brand']
    product.category = data['category']
    product.price = data['price']
    product.countInStock = data['countInStock']
    product.description = data['description']

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST',])
def uploadImage(request):
    data = request.data

    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()

    return Response('Image was uploaded')


@api_view(['POST',])
@permission_classes([permissions.IsAuthenticated,])
def createProductReview(request, pk):
    user = request.user
    data = request.data
    product = Product.objects.get(_id=pk)

    # Check if review already exists
    alreadyExists = product.product_reviews.filter(user=user).exists()

    if alreadyExists:
        content = {'detail': 'You have reviewed this product before!'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # Check if rating is 0
    elif data['rating'] == 0:
        content= {'detail': 'You should rate this product first!'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # Create Review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment']
        )

        totalReviews = product.product_reviews.all()
        numReviews = len(totalReviews)

        sumRate = 0
        for r in totalReviews:
            sumRate += r.rating
            
        avgRate = sumRate / numReviews

        product.rating = avgRate
        product.numReviews += 1
        product.save()

        return Response('Review is added')
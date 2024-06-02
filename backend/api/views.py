from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializer import *
from rest_framework.permissions import IsAuthenticated
from .models import Product,Customer,Order,OrderItem


@api_view(['POST'])
def Register_user(request):
    data=request.data
    serializer=Register(data=data)
    if serializer.is_valid():
        serializer.save()
        Customer.objects.create(
                user=serializer,
                name=serializer.data['username'],
                email=serializer.data['email'],
            )
        return Response({"status":201,"success":f"Account created for {serializer.data['username']}"})
    else:
        return Response({"status":400,
            "message":serializer.errors
            },status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def login_user(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    
    if not serializer.is_valid():
        return Response({
            "status": 400,
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
    
    if not user:
        return Response({
            "status": 400,
            "error": 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)
    else:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        return Response({
            'status': 200,
            'access': access_token,
            'refresh': refresh_token
        }, status=status.HTTP_200_OK)
    


@api_view(['POST'])
def add_product(request):
    data=request.data
    serializer=ProductSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status":201,"message":"Product added successfully"})
    return Response({"status":400,"message":serializer.errors})
        


@api_view(['GET'])
def products(request):
    products=Product.objects.all()
    serializer=ProductSerializer(products,many=True)
    return Response({"products":serializer.data})





@permission_classes([IsAuthenticated])
@api_view(['POST'])
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        serializer=OrderSerializer(order)
        serialized_order = serializer.data
        items = order.orderitem_set.all()
        serialized_items=ItemSerializer(items,many=True).data
        cartItems = order.get_cart_items
        cartTotal=order.get_cart_total
        new_serialized_items=[]
        for item in serialized_items:
            product=Product.objects.get(id=item['product'])
            item['categories']=ProductSerializer(product).data['categories']
            item['name']=ProductSerializer(product).data['name']
            item['image']=ProductSerializer(product).data['image']
            item['price']=ProductSerializer(product).data['price']
            item['cartTotal']=cartTotal
            item['items']=cartItems
            new_serialized_items.append(item)
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    #"order":serialized_order,
    context = {"status":200,"cartProducts":serialized_items}
    return Response(context)




def updateItem(request):
    data = request.data
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
        

    return Response({"message":"Item was added successfuly"}, safe=False)


from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializer import LoginSerializer,Register,ProductSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def Register_user(request):
    data=request.data
    serializer=Register(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status":200,"success":f"Account created for {serializer.data['username']}"})
    else:
        return Response({"status":"400",
            "message":serializer.errors
            },status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def login_user(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    
    if not serializer.is_valid():
        return Response({
            "status": False,
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
    
    if not user:
        return Response({
            "status": 400,
            "message": 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)
    
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
@permission_classes([IsAuthenticated])
def products(request):
    return Response({"Message":"products worked"})



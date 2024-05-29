from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product


from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class Register(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self,data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username is already taken")
        
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("Email already exists")

        return data

    def create(self,validated_data):
        user=User.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        
        return validated_data
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'



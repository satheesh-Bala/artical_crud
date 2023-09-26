from rest_framework import serializers
from api.models import ArticalModel
from django.contrib.auth.models import User

class ArticalSerializer(serializers.ModelSerializer):
    class Meta:
        model=ArticalModel
        fields='__all__'


class UserSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self, attrs):
        if User.objects.filter(username=attrs["username"]).exists():
             raise serializers.ValidationError("username already exists")
        return attrs
        
    def create(self, validated_data):
        user=User.objects.create(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return validated_data
    
class TokenSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
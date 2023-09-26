from django.shortcuts import HttpResponse
from rest_framework.decorators import APIView
from rest_framework.response import Response
from api.serializers import ArticalSerializer,UserSerializer,TokenSerializer
from api.models import ArticalModel
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


class ArticalCrud(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def post(self,request):
        data=request.data
        serializedData=ArticalSerializer(data=data)
        if serializedData.is_valid():
            serializedData.save()
            return Response(serializedData.data,status=201)
        else:
            return Response(serializedData.errors,status=400)
        
    def get(self,request):
        if request.data or request.GET.get('id'):
            print(request.GET.get('id'))
            try:
                if request.data:
                    print(request.GET.get('id'))
                    data=ArticalModel.objects.get(id=request.data['id'])
                else :
                    print(request.GET.get('id'))
                    data=ArticalModel.objects.get(id=request.GET.get('id'))
            except Exception as e:
                return Response({"error":f"{e}"},status=404)
            serializedData=ArticalSerializer(data)
            return Response(serializedData.data,status=200)
        data=ArticalModel.objects.all()
        serializedData=ArticalSerializer(data,many=True)
        return Response(serializedData.data,status=200)
    
    def put(self,request):
        dataput=request.data
        data=ArticalModel.objects.get(id=dataput['id'])
        seralizedData=ArticalSerializer(data,data=dataput)
        if seralizedData.is_valid():
            seralizedData.save()
            return Response(seralizedData.data,status=200)
        else:
            return Response(seralizedData.errors,status=404)
        
    def delete(self,request):
        ArticalModel.objects.get(id=request.data['id']).delete()
        return Response({"status":"deleted"},status=202)


class RegisterUser(APIView):

    def post(self,request):
        data=request.data
        serialize= UserSerializer(data=data)
        if serialize.is_valid():
            serialize.save()
            return Response({"status":"user created"},status=201)
        else:
            return Response(serialize._errors)
        
class CreateToken(APIView):
    
    def post(self,request):
        data=request.data
        serialize=TokenSerializer(data=data)
        if serialize.is_valid():
            user=authenticate(username=serialize.data["username"],password=serialize.data["password"])
            if user:
                tokenKey,_=Token.objects.get_or_create(user=user)
                return Response({"status":"found","Token":str(tokenKey)},status=201)
            else:
                return Response({"status":"not found"},status=404)
        else:
            return Response(serialize.errors)
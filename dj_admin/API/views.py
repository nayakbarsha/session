from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from .serializers import UserlistSerializer
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


# Create your views here.
@api_view(http_method_names=["GET"])
def userlist(request:Request):

    ulist = User.objects.all()
    serializer = UserlistSerializer(instance=ulist, many=True)
    response = {"message":"userlist", "data":serializer.data}

    return Response(data=response, status=status.HTTP_200_OK)

@api_view(http_method_names=["GET"])
def userdetail(request:Request, user_id:int):

    udetail = get_object_or_404(User, pk=user_id)
    serializer = UserlistSerializer(instance=udetail)
    response = {"message":"user data", "data": serializer.data}

    return Response(data=response, status=status.HTTP_200_OK)

@api_view(http_method_names=["POST"])
def adduser(request:Request):
    if request.method == "POST":
        data=request.data
        serializer = UserlistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {"message":"new user added", "data":data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=["PUT"])
def edituser(request:Request, user_id:int):

    udetail = get_object_or_404(User,pk=user_id)
    data = request.data
    serializer = UserlistSerializer(instance=udetail, data=data)
    if serializer.is_valid():
        serializer.save()
        response = {"message":"user updated succesfully", "data":serializer.data}
        return Response(data=response, status=status.HTTP_200_OK)
    
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(http_method_names=["DELETE"])
def deleteuser(request:Request, user_id:int):

    udetail = get_object_or_404(User,pk=user_id)
    udetail.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)




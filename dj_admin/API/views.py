from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from .serializers import UserlistSerializer
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


# Create your views here.

@api_view(http_method_names=["GET"])
def userlist(request:Request, user_id:int):

    ulist = get_object_or_404(User, pk=user_id)
    serializer = UserlistSerializer(instance=ulist)
    response = {"message":"userlist data", "data": serializer.data}

    return Response(data=response, status=status.HTTP_200_OK)
# from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import UserlistSerializer, ReviewSerializer
from rest_framework import status
from django.contrib.auth.models import User
from API.models import Review
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import mixins
# from rest_framework.permissions import IsAuthenticated
from API.permissions import IsOwnerOrReadOnly

# ----------------------function based views ---------------------------

# Create your views here.
# @api_view(http_method_names=["GET"])
# def userlist(request:Request):

#     ulist = User.objects.all()
#     serializer = UserlistSerializer(instance=ulist, many=True)
#     response = {"message":"userlist", "data":serializer.data}

#     return Response(data=response, status=status.HTTP_200_OK)

# @api_view(http_method_names=["POST"])
# def adduser(request:Request):
#     if request.method == "POST":
#         data=request.data
#         serializer = UserlistSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {"message":"new user added", "data":data}
#             return Response(data=response, status=status.HTTP_201_CREATED)
#         return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

# @api_view(http_method_names=["GET"])
# def userdetail(request:Request, user_id:int):

#     udetail = get_object_or_404(User, pk=user_id)
#     serializer = UserlistSerializer(instance=udetail)
#     response = {"message":"user data", "data": serializer.data}

#     return Response(data=response, status=status.HTTP_200_OK)


# @api_view(http_method_names=["PUT"])
# def edituser(request:Request, user_id:int):

#     udetail = get_object_or_404(User,pk=user_id)
#     data = request.data
#     serializer = UserlistSerializer(instance=udetail, data=data)
#     if serializer.is_valid():
#         serializer.save()
#         response = {"message":"user updated succesfully", "data":serializer.data}
#         return Response(data=response, status=status.HTTP_200_OK)
    
#     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(http_method_names=["DELETE"])
# def deleteuser(request:Request, user_id:int):

#     udetail = get_object_or_404(User,pk=user_id)
#     udetail.delete()

#     return Response(status=status.HTTP_204_NO_CONTENT)








# -------------------Mixins------------------------------
class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    


# -------------------Generics class based view----------------
class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserlistSerializer
    # permission_classes = [IsOwnerOrReadOnly]


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserlistSerializer
    # permission_classes = [IsOwnerOrReadOnly]


# ---------CLASS BASED VIEWS --------------------------------
# class UserList(APIView):
#     def get(self, request):
#         ulist = User.objects.all()
#         serializer = UserlistSerializer(instance=ulist, many=True)
#         response = {"message":"userlist", "data":serializer.data}

#         return Response(data=response, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         data=request.data
#         serializer = UserlistSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {"message":"new user added", "data":data}
#             return Response(data=response, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors)
        

# class Userdetails(APIView):
#     # permission_classes = [IsOwnerOrReadOnly]
#     def get(self, request, pk):
#         udetail = get_object_or_404(User, pk=pk)
#         serializer = UserlistSerializer(udetail)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         udetail = get_object_or_404(User, pk=pk)
#         data = request.data
#         serializer = UserlistSerializer(udetail, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {"message":"user updated succesfully", "data":serializer.data}
#             return Response(data=response, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self, request, pk):
#         udetail = get_object_or_404(User, pk=pk)
#         udetail.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import UserlistSerializer, ReviewSerializer
from rest_framework import status
from django.contrib.auth.models import User
from API.models import Review
# from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from API.permissions import IsReviewerOrReadOnly,IsOwnerOrReadOnly

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# ----------------------function based views ---------------------------

# Create your views here.
# @api_view(http_method_names=["GET"])
# def userlist(request:Request):

#     ulist = User.objects.all()
#     serializer = UserlistSerializer(instance=ulist, many=True)
#     response = {"message":"userlist", "data":serializer.data}

#     return Response(data=response, status=status.HTTP_200_OK)

@api_view(http_method_names=["POST"])
def adduser(request:Request):
    if request.method == "POST":
        data=request.data
        serializer = UserlistSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {"message":"new user added", "data":data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

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
    permission_classes = [IsReviewerOrReadOnly]



# ---------CLASS BASED VIEWS --------------------------------
class UserList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        ulist = User.objects.all()
        serializer = UserlistSerializer(instance=ulist, many=True)
        response = {"message":"userlist", "data":serializer.data}

        return Response(data=response, status=status.HTTP_200_OK)
    
    # def post(self, request):
    #     data=request.data
    #     serializer = UserlistSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         response = {"message":"new user added", "data":data}
    #         return Response(data=response, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors)
        

# class Userdetails(APIView):
#     def get(self, request, pk):
#         udetail = get_object_or_404(User, pk=pk)
#         serializer = UserlistSerializer(udetail)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         permission_classes = [IsOwnerOrReadOnly]
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



# -------------------Mixins------------------------------
class Userdetails( mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class =UserlistSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


















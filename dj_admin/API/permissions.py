from rest_framework import permissions

class IsReviewerOrReadOnly(permissions.BasePermission):

    # Custom permission to only allow owners of an object to edit it.

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user
        

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.username == request.user.username
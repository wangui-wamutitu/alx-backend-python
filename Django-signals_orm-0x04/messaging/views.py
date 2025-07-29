from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    # DELETE /users/delete-account/
    @action(detail=False, methods=["delete"], url_path="delete-account")
    def delete_user(self, request):
        user = request.user
        user.delete()
        return Response(
            {"detail": "Your account has been deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

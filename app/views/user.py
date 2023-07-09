from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from app.serializers import UserSerializer, UserLoginSerializer
from app.models import User 


# class CreateUser(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
class CreateUser(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):

    def post(self, request):
        # request.data (email, password)
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = User.objects.get(email=serializer.validated_data["email"])
                if user.password == serializer.validated_data["password"]:
                    token = Token.objects.get_or_create(user=user)
                    return Response({ "success": True, "token": token[0].key })
                else:
                    return Response({ "success": False, "message": "incorrect password" })

            except ObjectDoesNotExist:
                return Response({ "success": False, "message": "user does not exist" })


# class RetrieveUser(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
class RetrieveUser(APIView):
    def get(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateUser(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({ "success": True, "message": "user updated" }, status= status.HTTP_202_ACCEPTED)
        else:
            print(serializer.errors)
            return Response({ "success": False, "message": "error updating user" }, )



# class DestroyUser(generics.DestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def destroy(self, request, pk): 
#         try:
#             user = User.objects.get(id=pk)
#             if pk == request.user.id:
#                 self.perform_destroy(request.user)
#                 return Response({ "success": True, "message": "user deleted" },status= status.HTTP_202_ACCEPTED)
#             else:
#                 return Response({ "success": False, "message": "not enough permissions" }, status= status.HTTP_202_ACCEPTED)
#         except ObjectDoesNotExist:
#             return Response({ "success": False, "message": "user does not exist" }, status= status.HTTP_202_ACCEPTED)
class DestroyUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(id=pk)
            if pk == request.user.id:
                self.perform_destroy(request.user)
                return Response({"success": True, "message": "user deleted"}, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"success": False, "message": "not enough permissions"}, status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return Response({"success": False, "message": "user does not exist"}, status=status.HTTP_202_ACCEPTED)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import UserRegisterSerializer, UserLoginSerializer, ToDoItemSerializer
from .permissions import IsCreaterOrReadOnly
from todos.models import ToDoItem
from .swagger_configs import *


class RegisterView(APIView):

    @post_register_swagger
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response({"token": {'refresh': data['refresh'], 'access': data['access']}}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoItemCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ToDoItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoItemUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsCreaterOrReadOnly]

    def put(self, request, pk):
        todo_item = get_object_or_404(ToDoItem, pk=pk)
        self.check_object_permissions(request, todo_item)
        serializer = ToDoItemSerializer(todo_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoItemDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsCreaterOrReadOnly]

    def delete(self, request, pk):
        todo_item = get_object_or_404(ToDoItem, pk=pk)
        self.check_object_permissions(request, todo_item)
        todo_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToDoItemListView(APIView):
    permission_classes = [IsAuthenticated]

    @get_list_swagger
    def get(self, request):
        todo_items = ToDoItem.objects.all()
        serializer = ToDoItemSerializer(todo_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
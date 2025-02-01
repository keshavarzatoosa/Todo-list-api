from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import UserRegisterSerializer, UserLoginSerializer, ToDoItemSerializer
from .permissions import IsCreaterOrReadOnly
from todos.models import ToDoItem
from .swagger_configs import *
from .throttles import CustomUserRateThrottle, CustomRateThrottle


class RegisterView(APIView):

    @post_register_swagger
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response({"token": {'refresh': data['refresh'], 'access': data['access']}}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    @post_login_swagger
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoItemCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @post_todo_swagger
    def post(self, request):
        serializer = ToDoItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoItemUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsCreaterOrReadOnly]

    @put_todo_swagger
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

    @delete_todo_swagger
    def delete(self, request, pk):
        todo_item = get_object_or_404(ToDoItem, pk=pk)
        self.check_object_permissions(request, todo_item)
        todo_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToDoItemListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomRateThrottle]
    # throttle_classes = [CustomUserRateThrottle]
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]

    @get_list_swagger
    def get(self, request):
        todo_items = ToDoItem.objects.all()
        title = request.query_params.get('title')
        if title:
            todo_items = todo_items.filter(title__icontains=title)
        description = request.query_params.get('description')
        if description:
            todo_items = todo_items.filter(description__icontains=description)
        ordering = request.query_params.get('ordering')
        if ordering:
            todo_items = todo_items.order_by(ordering)
        serializer = ToDoItemSerializer(todo_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
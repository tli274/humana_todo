from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import ToDoListSerializer, UserSerializer
from .models import ToDoList

class ToDoListViewSet(viewsets.ModelViewSet):
    queryset = ToDoList.objects.all()
    serializer_class = ToDoListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ToDoList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class ToDoListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        todos = ToDoList.objects.all()
        serializer = ToDoListSerializer(todos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ToDoListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ToDoDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        todo = get_object_or_404(ToDoList, pk=pk)
        serializer = ToDoListSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk):
        todo = get_object_or_404(ToDoList, pk=pk)
        serializer = ToDoListSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = get_object_or_404(ToDoList, pk=pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# ------ AUTHENTICATION / AUTHORIZATION --------- 
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        
        return Response({"token": token.key}, status=status.HTTP_200_OK)

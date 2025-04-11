from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import ToDoList

class ToDoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoList
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
    
    def create(self, validated_data):
        role = validated_data.pop('role', 'user')
        user = User(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        
        user_group = Group.objects.get(name=role)
        user.groups.add(user_group)
        
        return user
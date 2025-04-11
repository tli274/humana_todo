from . import views
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, ToDoListViewSet, ToDoListView, ToDoDetailView, RegisterView
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'todos', ToDoListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('custom-todos/', ToDoListView.as_view()),
    path('custom-todos/<int:pk>', ToDoDetailView.as_view()),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
from django.urls import path
from rest_framework.routers import DefaultRouter
from todo import views


router = DefaultRouter()
router.register("groups", views.GroupViewSet)

urlpatterns = [
    path("todos/", views.TaskListCreate.as_view(), name="todo-list"),
    path("todos/<int:pk>/", views.TaskDetail.as_view(), name="todo-detail"),
] + router.urls
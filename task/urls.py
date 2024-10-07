from django.urls import path
from rest_framework.routers import DefaultRouter
from task import views


router = DefaultRouter()
router.register("groups", views.GroupViewSet)

urlpatterns = [
    path("tasks/", views.TaskListCreate.as_view(), name="task-list"),
    path("tasks/<int:pk>/", views.TaskDetail.as_view(), name="task-detail"),
] + router.urls
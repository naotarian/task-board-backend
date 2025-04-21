from django.urls import path
from .views import ProjectCreateView, ProjectDetailView, ProjectListView

urlpatterns = [
  path('create/', ProjectCreateView.as_view(), name='project-create'),
  path("<str:pk>/", ProjectDetailView.as_view(), name="project-detail"),
  path("", ProjectListView.as_view(), name="project-list"),
]

from django.urls import path
from .views import ProjectCreateView, ProjectDetailView

urlpatterns = [
  path('', ProjectCreateView.as_view(), name='project-create'),
  path("<str:pk>/", ProjectDetailView.as_view(), name="project-detail"),
]

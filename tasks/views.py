from djeden.views import ListView, DetailView
from rest_framework.generics import ListCreateAPIView

from .models import Task
from .serializers import TaskSerializer


# class TaskList(ListView):
class TaskList(ListCreateAPIView):
	"""
	List all the projects or create a new project.
	"""
	model = Task
	serializer_class = TaskSerializer


class TaskDetail(DetailView):
	model = Task
	serializer_class = TaskSerializer

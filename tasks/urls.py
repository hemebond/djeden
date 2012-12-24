from django.conf.urls import patterns, url
from .views import TaskList, TaskDetail

urlpatterns = patterns('tasks.views',
	url(r'^$', TaskList.as_view(), name='task-list'),
	url(r'^(?P<pk>\d+)/$', TaskDetail.as_view(), name='task-detail'),
)

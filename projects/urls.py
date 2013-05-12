from django.conf.urls import patterns, url
from .views import ProjectList, ProjectDetail, TaskList, TaskDetail


urlpatterns = patterns('projects.views',
	url(
		r'^(?:(?P<url_method>create)/)?$',
		ProjectList.as_view(),
		name='project_list'
	),
	url(
		r'^(?P<pk>\d+)/(?:(?P<url_method>read|update|delete)/)?$',
		ProjectDetail.as_view(),
		name='project_detail'
	),
	url(
		r'^(?P<pk>\d+)/tasks/(?:(?P<url_method>create)/)?$',
		TaskList.as_view(),
		name='project_task_list'
	),
	url(
		r'^(?P<project_pk>\d+)/tasks/(?P<pk>\d+)/$',
		TaskDetail.as_view(),
		name='project_task_detail'
	),
)

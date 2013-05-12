from django.core.urlresolvers import reverse
from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from djeden.utils import table_from_list, detail_from_dict, table_from_qs
from djeden.views import ListView
from djeden.views import DetailView

from rest_framework.response import Response

from .models import Project, ProjectOrganisation, Task
from .serializers import ProjectSerializer, TaskSerializer
from .forms import ProjectForm, TaskForm


def menu():
	return [
		{
			'label': _("Projects"),
			'items': [
				{
					'label': _("List"),
					'url': reverse('project_list'),
				},
				{
					'label': _("New"),
					'url': reverse(
						'project_list',
						kwargs={
							'url_method': "create"
						}
					),
				},
				{
					'label': _("Map"),
					'url': "",
				},
			]
		},
		{
			'label': _("Reports"),
			'items': [
				{
					'label': _("List"),
					'url': "",
				},
				{
					'label': _("3W"),
					'url': "",
				},
				{
					'label': _("Funding"),
					'url': "",
				},
			]
		},
		{
			'label': _("Import"),
			'items': [
				{
					'label': _("Projects"),
					'url': "",
				},
				{
					'label': _("Project Organisations"),
					'url': "",
				},
				{
					'label': _("Project Locations"),
					'url': "",
				},
			]
		},
		{
			'label': _("Partner Organisations"),
			'items': [
				{
					'label': _("List"),
					'url': "",
				},
				{
					'label': _("New"),
					'url': "",
				},
				{
					'label': _("Import"),
					'url': "",
				},
			]
		},
		{
			'label': _("Themes"),
			'items': [
				{
					'label': _("List"),
					'url': "",
				},
				{
					'label': _("New"),
					'url': "",
				},
			]
		},
		{
			'label': _("Activity Types"),
			'items': [
				{
					'label': _("List"),
					'url': "",
				},
				{
					'label': _("New"),
					'url': "",
				},
			]
		},
		{
			'label': _("Haz"),
			'items': [
				{
					'label': _("New"),
					'url': "",
				},
				{
					'label': _("List All"),
					'url': "",
				},
			]
		},
	]


class ProjectOrganisationForm(forms.ModelForm):
	class Meta:
		model = ProjectOrganisation


class ProjectList(ListView):
	model = Project
	serializer_class = ProjectSerializer
	form_class = ProjectForm
	fields = [
		'name',
		'code',
		'sectors',  # list
		'countries',  # list
		'hazards',  # list
		'themes',  # list
		'start_date',
		'end_date',
		'organisations',  # list
	]

	def get_context_data(self, *args, **kwargs):
		context = super(ProjectList, self).get_context_data(*args, **kwargs)

		context['module_menu'] = menu()
		context['breadcrumbs'] = [
			{
				'label': _("Projects"),
			},
		]
		context['table'] = table_from_qs(
			self.object_list,
			self.fields,
		)
		context['form_action'] = reverse('project_list')

		return context

	def get_success_url(self):
		return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectDetail(DetailView):
	model = Project
	serializer_class = ProjectSerializer
	form_class = ProjectForm

	def get_context_data(self, *args, **kwargs):
		context = super(ProjectDetail, self).get_context_data(*args, **kwargs)
		context['project'] = self.object
		context['breadcrumbs'] = [
			{
				'label': _("Projects"),
				'url': reverse('project_list')
			},
			{
				'label': _(u"%s" % self.object),
			},
			{
				'label': _("Detail"),
				'menu': [
					{
						'label': _("Organisations"),
					},
					{
						'label': _("Locations"),
					},
					{
						'label': _("Activities"),
					},
					{
						'label': _("Tasks"),
						'url': reverse(
							'project_task_list',
							kwargs={'pk': self.object.pk}
						),
					},
					{
						'label': _("Documents"),
					},
					{
						'label': _("Staff"),
					},
					{
						'label': _("Volunteers"),
					},
				]
			}
		]
		context['module_menu'] = menu()
		context['data'] = detail_from_dict(self.model, self.serializer_class(self.object).data)
		return context

	def get_success_url(self):
		return reverse('project_detail', kwargs={'pk': self.object.pk})


class TaskList(ListView):
	"""
	List all the tasks or create a new task.
	"""
	model = Task
	serializer_class = TaskSerializer
	form_class = TaskForm
	fields = [
		"name",
		"task_type",
		"priority",
		"severity",
		"resolution",
		"created",
		"modified",
	]

	def get_queryset(self):
		project = get_object_or_404(Project, pk=self.kwargs['pk'])
		return Task.objects.filter(project=project)

	def get_context_data(self, *args, **kwargs):
		context = super(TaskList, self).get_context_data(*args, **kwargs)
		context['project'] = get_object_or_404(Project, pk=self.kwargs['pk'])
		context['breadcrumbs'] = [
			{
				'label': _("Projects"),
				'url': reverse('project_list')
			},
			{
				'label': _(u"%s" % context['project']),
			},
			{
				'label': _("Tasks"),
				'menu': [
					{
						'label': _("Detail"),
						'url': reverse('project_detail', kwargs={'pk': self.kwargs['pk']}),
					},
					{
						'label': _("Organisations"),
					},
					{
						'label': _("Locations"),
					},
					{
						'label': _("Activities"),
					},
					{
						'label': _("Documents"),
					},
					{
						'label': _("Staff"),
					},
					{
						'label': _("Volunteers"),
					},
				]
			}
		]
		context['menu'] = menu()

		context['table'] = table_from_list(Task, self.fields, context['serialized_data'])
		return context


class TaskDetail(DetailView):
	model = Task
	serializer_class = TaskSerializer
	form_class = TaskForm

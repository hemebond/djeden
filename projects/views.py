from django.core.urlresolvers import reverse
from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from djeden.views import ListView
from djeden.views import DetailView

from rest_framework.response import Response

from .models import Project, ProjectOrganisation, Task
from .serializers import ProjectSerializer, TaskSerializer


def menu():
	return [
		{
			'label': _("Projects"),
			'items': [
				{
					'label': _("List"),
					'url': reverse('project-list'),
				},
				{
					'label': _("New"),
					'url': reverse('project-list', kwargs={'url_method': "create"}),
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
					'label': _("New"),
					'url': "",
				},
				{
					'label': _("List All"),
					'url': "",
				},
				{
					'label': _("Search"),
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
					'label': _("New"),
					'url': "",
				},
				{
					'label': _("List All"),
					'url': "",
				},
			]
		},
		{
			'label': _("Activity Types"),
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

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		exclude = ('organisations', )
		widgets = {
			'hazards': forms.CheckboxSelectMultiple(),
			'hfas': forms.CheckboxSelectMultiple(),
			'themes': forms.CheckboxSelectMultiple(),
			'sectors': forms.CheckboxSelectMultiple(),
		}

	def __init__(self, *args, **kwargs):
		super(ProjectForm, self).__init__(*args, **kwargs)
		self.fields['hazards'].help_text = ""
		self.fields['hfas'].help_text = ""
		self.fields['themes'].help_text = ""
		self.fields['sectors'].help_text = ""

	def save(self, force_insert=False, force_update=False, commit=True):
		project = super(ProjectForm, self).save(commit=False)

		if commit:
			project.save()
			self.save_m2m()

		return project


class ProjectOrganisationForm(forms.ModelForm):
	class Meta:
		model = ProjectOrganisation


class ProjectList(ListView):
	model = Project
	serializer_class = ProjectSerializer
	form_class = ProjectForm

	def get_context_data(self, *args, **kwargs):
		context = super(ProjectList, self).get_context_data(*args, **kwargs)
		context['menu'] = menu()
		return context

	def get_success_url(self):
		return reverse('project-detail', kwargs={'pk': self.object.pk})


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
				'url': reverse('project-list')
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
						'url': reverse('project-task-list', kwargs={'pk': self.object.pk}),
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
		return context

	def get_success_url(self):
		return reverse('project-detail', kwargs={'pk': self.object.pk})


class TaskForm(forms.ModelForm):
	class Meta:
		model = Task


class TaskList(ListView):
	"""
	List all the tasks or create a new task.
	"""
	model = Task
	serializer_class = TaskSerializer
	form_class = TaskForm

	def get_queryset(self):
		return Task.objects.filter(project_id=self.kwargs['pk'])

	def get_context_data(self, *args, **kwargs):
		context = super(TaskList, self).get_context_data(*args, **kwargs)
		context['project'] = get_object_or_404(Project, pk=self.kwargs['pk'])
		context['breadcrumbs'] = [
			{
				'label': _("Projects"),
				'url': reverse('project-list')
			},
			{
				'label': _(u"%s" % context['project']),
			},
			{
				'label': _("Tasks"),
				'menu': [
					{
						'label': _("Detail"),
						'url': reverse('project-detail', kwargs={'pk': self.kwargs['pk']}),
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
		return context


class TaskDetail(DetailView):
	model = Task
	serializer_class = TaskSerializer
	form_class = TaskForm

from django import forms

from .models import Project, Task


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = [
			'name',
			'code',
			'description',
			'status',
			'start_date',
			'end_date',
			'currency',
			'hazards',
			'hfas',
			'sectors',
			'themes',
		]
		# widgets = {
		# 	'hazards': forms.CheckboxSelectMultiple(),
		# 	'hfas': forms.CheckboxSelectMultiple(),
		# 	'themes': forms.CheckboxSelectMultiple(),
		# 	'sectors': forms.CheckboxSelectMultiple(),
		# }

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


class TaskForm(forms.ModelForm):
	class Meta:
		model = Task

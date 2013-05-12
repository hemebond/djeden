from django.shortcuts import HttpResponseRedirect
from django.forms.models import modelform_factory


class SimpleFormMixin(object):
	form_class = None
	success_url = None

	def get_initial(self):
		return {}

	def get_form_kwargs(self):
		kwargs = {}

		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
				'data': self.request.POST,
				'files': self.request.FILES,
			})
		return kwargs

	def get_form_class(self):
		"""
		Returns the form class to use in this view
		"""
		if self.form_class:
			return self.form_class
		else:
			if self.model is not None:
				# If a model has been explicitly provided, use it
				model = self.model
			else:
				# Try to get a queryset and extract the model class
				# from that
				model = self.get_queryset().model

		return modelform_factory(model)

	def get_form(self):
		"""
			Returns a list of form objects
		"""
		return self.get_form_class()(**self.get_form_kwargs())

	def get_formsets(self):
		"""
			Returns a list of formsets
		"""
		return []

	def get_success_url(self):
		return self.success_url

	def form_valid(self, form):
		return HttpResponseRedirect(self.get_success_url())


class SimpleModelFormMixin(SimpleFormMixin):
	def form_valid(self, form):
		self.object = form.save()
		return super(SimpleModelFormMixin, self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(SimpleModelFormMixin, self).get_form_kwargs()
		kwargs.update({'instance': self.object})
		return kwargs

import json

# from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
# from django.forms import ModelForm

from rest_framework.settings import api_settings
from rest_framework.decorators import APIView
from rest_framework.response import Response
# from rest_framework import status
from rest_framework.reverse import reverse as rest_reverse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

# from django.views.generic.list import MultipleObjectTemplateResponseMixin
# from django.views.generic.detail import SingleObjectTemplateResponseMixin
# from django.views.generic.edit import ModelFormMixin

from .mixins import SimpleFormMixin
from .mixins import SimpleModelFormMixin
from .utils import JSONEncoder


class Root(APIView):
	def get(self, request):
		return Response({
			'projects': rest_reverse('project_list', request=request),
			'organisations': rest_reverse('organisation_list', request=request),
		})


class ListView(SimpleFormMixin, ListCreateAPIView):
	renderer_classes = [TemplateHTMLRenderer, ] \
	                 + api_settings.DEFAULT_RENDERER_CLASSES
	model = None
	serializer_class = None
	form_class = None
	success_url = None
	template_name_suffix = "_list"

	def get_template_names(self):
		try:
			names = super(ListView, self).get_template_names()
		except AttributeError:
			names = []

		# Add a path to a custom list template
		if hasattr(self, 'model') and hasattr(self.model, '_meta'):
			opts = self.model._meta
			names.append("%s/%s%s.html" % (
				opts.app_label,
				opts.object_name.lower(),
				self.template_name_suffix
			))

			# the default list view template
			if self.template_name_suffix == "_form":
				names.append("form.html")

			names.append("list.html")

		return names

	def get(self, request, *args, **kwargs):
		format = request.accepted_renderer.format
		method = kwargs.get('url_method', None)

		if format == 'html':
			if method == 'create':
				self.template_name_suffix = "_form"

			queryset = self.get_queryset()
			self.object_list = self.filter_queryset(queryset)
			form = self.get_form_class()(**self.get_form_kwargs())
			serialized_data = self.serializer_class(self.object_list).data

			context = self.get_context_data(
				object_list=self.object_list,
				serialized_data=serialized_data,
				json=json.dumps(serialized_data, cls=JSONEncoder),
				form=form,
			)

			return Response(context)

		# remove TemplateHTMLRenderer to fix the API preview
		self.renderer_classes.pop(0)

		return super(ListView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		format = request.accepted_renderer.format

		if format == 'html':
			form = self.get_form_class()(**self.get_form_kwargs())

			if form.is_valid():
				self.object = form.save()
				return HttpResponseRedirect(self.get_success_url())

			self.template_name_suffix = "_form"

			queryset = self.get_queryset()
			self.object_list = self.filter_queryset(queryset)

			context = self.get_context_data(
				object_list=self.object_list,
				form=form
			)

			return Response(context)

		# remove TemplateHTMLRenderer to fix the API preview
		self.renderer_classes.pop(0)

		return super(ListView, self).post(request, *args, **kwargs)


class DetailView(SimpleModelFormMixin, RetrieveUpdateAPIView):
	renderer_classes = [TemplateHTMLRenderer, ] \
	                 + api_settings.DEFAULT_RENDERER_CLASSES
	template_name_suffix = "_detail"

	def get_template_names(self):
		try:
			names = super(DetailView, self).get_template_names()
		except AttributeError:
			names = []

		# Add a path to a custom list template
		if hasattr(self, 'model') and hasattr(self.model, '_meta'):
			opts = self.model._meta
			names.append("%s/%s%s.html" % (
				opts.app_label,
				opts.object_name.lower(),
				self.template_name_suffix
			))

			# the default list view template
			if self.template_name_suffix == "_form":
				names.append("form.html")

			names.append("detail.html")

		return names

	def get_context_data(self, *args, **kwargs):
		context = super(DetailView, self).get_context_data(*args, **kwargs)
		context.update({
			'form': self.get_form_class()(**self.get_form_kwargs()),
			'form_action': reverse(
				'project_detail',
				kwargs={
					'pk': self.object.pk
				}
			),
		})

		return context

	def get(self, request, *args, **kwargs):
		format = request.accepted_renderer.format
		method = kwargs.get('url_method', None)

		if format == 'html':
			self.object = self.get_object()

			context = self.get_context_data(
				object=self.object
			)

			if method == 'update':
				self.template_name_suffix = "_form"

			return Response(context)

		# remove TemplateHTMLRenderer to fix the API preview
		self.renderer_classes.pop(0)

		return super(DetailView, self).get(request, *args, **kwargs)

	def form_invalid(self, form):
		self.template_name_suffix = "_form"
		return Response({
			'form': form,
			'form_action': "",
		})

	def post(self, request, *args, **kwargs):
		format = request.accepted_renderer.format

		self.object = self.get_object()

		if format == 'html':
			form = self.get_form()

			if form.is_valid():
				return self.form_valid(form)
			else:
				return self.form_invalid(form)

		# remove TemplateHTMLRenderer to fix the API preview
		self.renderer_classes.pop(0)

		return super(DetailView, self).post(request, *args, **kwargs)

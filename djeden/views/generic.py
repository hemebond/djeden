from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.models import modelform_factory

from rest_framework.settings import api_settings
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse as restreverse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.generics import ListCreateAPIView

from django.views.generic.list import MultipleObjectTemplateResponseMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin

from rest_framework import mixins
from rest_framework import generics

from djeden.mixins import SimpleModelFormMixin


class Root(APIView):
	def get(self, request):
		return Response({
			'projects': restreverse('project-list', request=request),
			'organisations': restreverse('organisation-list', request=request),
		})


class ListView(MultipleObjectTemplateResponseMixin, ListCreateAPIView):
	renderer_classes = [TemplateHTMLRenderer, ] + api_settings.DEFAULT_RENDERER_CLASSES
	model = None
	serializer_class = None
	form_class = None
	success_url = None

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

	def get_template_names(self):
		try:
			names = super(ListView, self).get_template_names()
		except AttributeError:
			names = []

		if hasattr(self, 'model') and hasattr(self.model, '_meta'):
			opts = self.model._meta
			names.append("%s/%s%s.html" % (
				opts.app_label,
				opts.object_name.lower(),
				self.template_name_suffix
			))

		return names

	def get(self, request, *args, **kwargs):
		format = request.accepted_renderer.format
		method = kwargs.get('url_method', None)

		if method == 'create':
			if format != 'html':
				return Response(status=status.HTTP_404_NOT_FOUND)

			self.template_name_suffix = "_form"

			form = self.get_form_class()()
			context = self.get_context_data(object_list=[], form=form)

			return Response(context)

		if format == 'html':
			context = self.get_context_data(object_list=self.get_queryset())
			return Response(context)

		return super(ListView, self).get(request, *args, **kwargs)

	def get_success_url(self):
		if self.success_url:
			url = self.success_url % self.object.__dict__
		else:
			try:
				url = self.object.get_absolute_url()
			except AttributeError:
				raise ImproperlyConfigured(
					"No URL to redirect to. Either provide a url or define"
					" a get_absolute_url method on the Model.")
		return url

	def post(self, request, *args, **kwargs):
		format = request.accepted_renderer.format

		if format == 'html':
			form = self.get_form_class()(request.POST)

			if form.is_valid():
				self.object = form.save()
				return HttpResponseRedirect(self.get_success_url())

			self.template_name_suffix = "_form"
			context = self.get_context_data(object_list=[], form=form)
			return Response(context)

		return super(ListView, self).post(request, *args, **kwargs)


class DetailView(mixins.RetrieveModelMixin,
	             mixins.UpdateModelMixin,
	             mixins.DestroyModelMixin,
	             generics.SingleObjectAPIView,
	             SimpleModelFormMixin,
	             SingleObjectTemplateResponseMixin):
 	renderer_classes = [TemplateHTMLRenderer, ] + api_settings.DEFAULT_RENDERER_CLASSES
 	context_object_name = "object"

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()

		format = request.accepted_renderer.format
		method = kwargs.get('url_method', None)

		if format == 'html':
			context = self.get_context_data()
			context.update({
				'form': self.get_form(),
				'form_action': reverse(
					'project-detail',
					kwargs={
						'pk': self.object.pk
					}
				),
			})

			if method == 'update':
				self.template_name_suffix = "_form"

			return Response(context)

		return self.retrieve(request, *args, **kwargs)

	def form_invalid(self, form):
		self.template_name_suffix = "_form"
		return Response({
			'form': form,
			'form_action': "",
		})

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()

		format = request.accepted_renderer.format
		# method = kwargs['url_method']

		if format == 'html':
			form = self.get_form()

			if form.is_valid():
				return self.form_valid(form)
			else:
				return self.form_invalid(form)

		return self.update(request, *args, **kwargs)

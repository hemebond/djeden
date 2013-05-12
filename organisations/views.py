import json

# from string import capwords

from rest_framework.settings import api_settings
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect
from django import forms

from djeden.utils import table_from_list, detail_from_dict, table_from_qs
from djeden.views import ListView, DetailView

from kapua.locations.serializers import OfficeSerializer
from kapua.locations.models import Location, Country

from .models import Organisation, OrganisationType
from .filters import OrganisationFilter
from .forms import OrganisationForm
from .serializers import (
	OrganisationSerializer,
	OrganisationTypeSerializer
)


def menu(current_url=None):
	menu = [
		{
			'label': _("Organisations"),
			'items': [
				{
					'label': _("List"),
					'url': reverse('organisation_list'),
				},
				{
					'label': _("New"),
					'url': reverse(
						'organisation_list',
						kwargs={'url_method': "create"}
					),
				},
				{
					'label': _("Import"),
					'url': "",
				}
			]
		},
		{
			'label': _("Offices"),
			'items': [
				{
					'label': _("List"),
					'url': reverse('organisation_office_list'),
				},
				{
					'label': _("New"),
					'url': reverse(
						'organisation_office_list',
						kwargs={'url_method': "create"}
					),
				},
				{
					'label': _("Import"),
					'url': "",
				},
			]
		},
		{
			'label': _("Facilities"),
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
			'label': _("Organisation Types"),
			'items': [
				{
					'label': _("List"),
					'url': reverse('organisation_type_list'),
				},
				{
					'label': _("New"),
					'url': reverse(
						'organisation_type_list',
						kwargs={'url_method': "create"},
					),
				},
			]
		},
		{
			'label': _("Office Types"),
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
			'label': _("Facility Types"),
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
			'label': _("Sectors"),
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
	]

	if current_url:
		for group in menu:
			for item in group['items']:
				if item['url'] == current_url:
					item['active'] = True

	return menu





def cell(field,
         label=None,
         type="string",
         url=None):
	return


class OfficeForm(forms.Form):
	COUNTRIES = (
		(x.id, x.name) for x in Country.objects.all()
	)
	country = forms.CharField(
		max_length=255,
		widget=forms.Select(choices=COUNTRIES)
	)
	office = forms.CharField(max_length=255)


class OrganisationList(ListView):
	model = Organisation
	serializer_class = OrganisationSerializer
	filter_class = OrganisationFilter
	success_url = "/organisations/"

	def get_success_url(self):
		return reverse(
			'organisation_detail',
			kwargs={'pk': self.object.pk},
		)

	def get_context_data(self, *args, **kwargs):
		context = super(OrganisationList, self).get_context_data(*args, **kwargs)

		fields = [
			{
				'name': "name",
				# 'verbose_name': "name",
				# 'type': "string",
			},
			{
				'name': "acronym",
				# 'verbose_name': "acronym",
				# 'type': "string",
			},
			{
				'name': "orgtype",
				# 'verbose_name': "type",
				# 'type': "string",
			},
			{
				'name': "sectors",
				# 'verbose_name': "sectors",
				# 'type': "list",
			},
			{
				'name': "country",
				# 'verbose_name': "home country",
				# 'type': "string",
			},
			{
				'name': "website",
				# 'verbose_name': "website",
				# 'type': "url",
			},
		]

		print context['serialized_data']

		context['table'] = table_from_list(
			context['serialized_data'],
			self.model,
			fields,
		)

		# context['table'] = table_from_qs(
		# 	self.object_list.queryset,
		# 	field_list=fields
		# )

		context['module_menu'] = menu(self.request.path)
		context['breadcrumbs'] = [
			{
				'label': _("Organisations"),
			},
		]

		context['form_action'] = reverse('organisation_list')

		context['tabs'] = ['maps']

		context['json'] = json.dumps(context['serialized_data'])

		context['filter'] = OrganisationFilter(self.request.GET)

		return context


class OrganisationDetail(DetailView):
	renderer_classes = [TemplateHTMLRenderer, ] + api_settings.DEFAULT_RENDERER_CLASSES
	model = Organisation
	serializer_class = OrganisationSerializer

	def get_initial(self):
		return {}

	def get_form_kwargs(self):
		"""
		Returns the keyword arguments for instantiating the form.
		"""
		kwargs = super(OrganisationDetail, self).get_form_kwargs()
		kwargs.update({'instance': self.object})
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(OrganisationDetail, self).get_context_data(*args, **kwargs)

		serializer = self.serializer_class(self.object)

		context['data'] = detail_from_dict(
			self.model,
			fields=[
				"name",
				"acronym",
				"orgtype",
				"website",
				"sectors",
				"country",
			],
			data=serializer.data
		)
		context['module_menu'] = menu()
		context['breadcrumbs'] = [
			{
				'label': _("Organisations"),
				'url': reverse('organisation_list')
			},
			{
				'label': _(u"%s" % self.object),
			},
			{
				'label': _("Detail"),
				'menu': [
					{
						'label': _("Branches"),
					},
					{
						'label': _("Offices"),
						'url': reverse(
							'organisation_component_office_list',
							kwargs={
								'pk': self.object.pk,
							}
						),
					},
					{
						'label': _("Warehouses"),
					},
					{
						'label': _("Facilities"),
					},
					{
						'label': _("Staff & Volunteers"),
					},
					{
						'label': _("Assets"),
					},
					{
						'label': _("Projects"),
					},
					{
						'label': _("User Roles"),
					},
				]
			}
		]

		if "form" not in context:
			context['form'] = OrganisationForm(**self.get_form_kwargs())

		context['form_action'] = reverse(
			'organisation_detail',
			kwargs={'pk': self.object.pk},
		)

		return context

	def get(self, request, *args, **kwargs):
		format = request.accepted_renderer.format
		method = kwargs.get('url_method', None)

		if format == 'html':
			self.object = self.get_object()
			context = self.get_context_data(object=self.object)

			if method == 'update':
				template_name = "form.html"
			else:
				template_name = "detail.html"

			return Response(
				context,
				template_name=template_name,
			)

		return super(OrganisationDetail, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		format = request.accepted_renderer.format

		if format == 'html':
			self.object = self.get_object()
			form = OrganisationForm(**self.get_form_kwargs())

			if form.is_valid():
				self.object = form.save()
				return HttpResponseRedirect(
					reverse(
						'organisation_detail',
						kwargs={
							'pk': self.object.pk,
						}
					)
				)
			else:
				context = self.get_context_data(
					object=self.object,
					form=form,
				)

				return Response(
					context,
					template_name="form.html",
				)

		return super(OrganisationDetail, self).post(request, *args, **kwargs)


class OrganisationTypeList(ListCreateAPIView):
	model = OrganisationType
	serializer_class = OrganisationTypeSerializer


class OrganisationTypeDetail(RetrieveUpdateDestroyAPIView):
	model = OrganisationType
	serializer_class = OrganisationTypeSerializer


class OrganisationOfficeList(ListCreateAPIView):
	renderer_classes = [TemplateHTMLRenderer, ] + api_settings.DEFAULT_RENDERER_CLASSES
	model = Location
	serializer_class = OfficeSerializer

	def get_queryset(self):
		return self.parent_object.offices.all()

	def get_context_data(self, *args, **kwargs):
		context = super(OrganisationOfficeList, self).get_context_data(*args, **kwargs)

		serializer = self.serializer_class(self.object_list)

		fields = [
			{
				'name': "name",
				'url': "",
				# 'verbose_name': "name",
				# 'type': "string",
			},
		]

		context['table'] = table_from_list(
			self.model,
			fields,
			serializer.data
		)
		context['module_menu'] = menu()
		context['breadcrumbs'] = [
			{
				'label': _("Organisations"),
				'url': reverse('organisation_list')
			},
			{
				'label': _(u"%s" % self.parent_object),
			},
			{
				'label': _("Offices"),
				'menu': [
					{
						'label': _("Detail"),
						'url': reverse(
							'organisation_detail',
							kwargs={
								'pk': self.parent_object.pk
							}
						)
					},
					{
						'label': _("Branches"),
					},
					{
						'label': _("Warehouses"),
					},
					{
						'label': _("Facilities"),
					},
					{
						'label': _("Staff & Volunteers"),
					},
					{
						'label': _("Assets"),
					},
					{
						'label': _("Projects"),
					},
					{
						'label': _("User Roles"),
					},
				]
			}
		]

		return context

	def get(self, request, *args, **kwargs):
		format = request.accepted_renderer.format
		method = kwargs.get('url_method', None)

		self.parent_object = Organisation.objects.get(pk=self.kwargs.get('pk'))

		if format == 'html':
			queryset = self.get_queryset()
			self.object_list = self.filter_queryset(queryset)
			context = self.get_context_data(object_list=self.object_list)

			if method == 'create':
				template_name = "form.html"
			else:
				template_name = "list.html"

			return Response(
				context,
				template_name=template_name,
			)

		return super(OrganisationOfficeList, self).get(request, *args, **kwargs)


class OfficeList(ListCreateAPIView):
	renderer_classes = [TemplateHTMLRenderer, ] + api_settings.DEFAULT_RENDERER_CLASSES
	model = Location
	serializer_class = OfficeSerializer

	def get_queryset(self):
		queryset = super(OfficeList, self).get_queryset()
		return queryset.filter(type__name="office")

	def get_context_data(self, *args, **kwargs):
		context = super(OfficeList, self).get_context_data(*args, **kwargs)

		serializer = self.serializer_class(self.object_list)

		fields = [
			{
				'name': "name",
				'url': "",
				# 'verbose_name': "name",
				# 'type': "string",
			},
			{
				'name': "country",
			},
			{
				'name': "ancestors",
			},
		]

		context['table'] = table_from_list(
			self.model,
			fields,
			serializer.data
		)
		context['module_menu'] = menu(self.request.path)
		context['breadcrumbs'] = [
			{
				'label': _("Offices"),
			},
		]

		return context

	def get(self, request, *args, **kwargs):
		format = request.accepted_renderer.format
		method = kwargs.get('url_method', None)

		if format == 'html':
			queryset = self.get_queryset()
			self.object_list = self.filter_queryset(queryset)
			context = self.get_context_data(object_list=self.object_list)

			if method == 'create':
				template_name = "form.html"
			else:
				template_name = "list.html"

			return Response(
				context,
				template_name=template_name,
			)

		return super(OfficeList, self).get(request, *args, **kwargs)

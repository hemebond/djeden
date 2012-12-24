from rest_framework.settings import api_settings
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponseRedirect
from django.db.models.fields import FieldDoesNotExist
from django import forms

from organisations.models import Organisation, OrganisationType
from organisations.serializers import OrganisationSerializer, OrganisationTypeSerializer

from string import capwords

from djeden.mixins import SimpleModelFormMixin

from djeden.mixins import SimpleFormMixin
def menu():
	return [
		{
			'label': _("Organisations"),
			'items': [
				{
					'label': _("Add Organisation"),
					'url': reverse(
						'organisation-list',
						kwargs={'url_method': "create"}
					),
				},
				{
					'label': _("List All"),
					'url': reverse('organisation-list'),
					'active': True,
				},
				{
					'label': _("Search"),
					'url': "",
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
					'label': _("New"),
					'url': "",
				},
				{
					'label': _("List All"),
					'url': "",
				},
				{
					'label': _("Map"),
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
			'label': _("Facilities"),
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
					'label': _("Map"),
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
			'label': _("Organisation Types"),
			'items': [
				{
					'label': _("New"),
					'url': reverse(
						'organisation-type-list',
						kwargs={'url_method': "create"},
					),
				},
				{
					'label': _("List All"),
					'url': reverse('organisation-type-list'),
				},
			]
		},
		{
			'label': _("Office Types"),
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
			'label': _("Facility Types"),
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
			'label': _("Sectors"),
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


def table_from_list(model, fields, data):
	table = {
		'columns': [],
		'records': [],
	}

	for field in fields:
		column = {}

		if 'verbose_name' in field:
			label = field['verbose_name']
		else:
			label = model._meta \
						 .get_field(field['name']) \
						 .verbose_name
		column['label'] = label

		table['columns'].append(column)

	for obj in data:
		record = {
			'pk': obj['pk'],
			'cells': [],
		}

		for field in fields:
			cell = {
				'name': field['name'],
				'value': obj[field['name']],
				'type': field.get('type', None),
			}

			if "name" == field['name']:
				cell.update({'url': obj['url']})

			record['cells'].append(cell)

		table['records'].append(record)

	return table


def detail_from_dict(model, fields, data):
	"""
	data is serializer.data
	"""

	detail = []
	print data

	if not fields:
		fields = data.keys()

	for field in fields:
		try:
			label = model._meta.get_field(field).verbose_name
		except FieldDoesNotExist:
			label = field

		value = data[field]

		if isinstance(value, list):
			field_type = "list"
		else:
			field_type = "string"

		detail.append({
			'field': field,
			'label': label,
			'value': value,
			'type': field_type,
		})

	return detail


class OrganisationForm(forms.ModelForm):
	class Meta:
		model = Organisation


class OrganisationList(SimpleFormMixin, ListCreateAPIView):
	renderer_classes = [TemplateHTMLRenderer, ] + api_settings.DEFAULT_RENDERER_CLASSES
	model = Organisation
	serializer_class = OrganisationSerializer

	def get_filtered_queryset(self):
		"""
			Fetch the filtered queryset and then order it by name
		"""
		queryset = super(OrganisationList, self).get_filtered_queryset()
		return queryset.order_by('name')

	def get_context_data(self, *args, **kwargs):
		context = super(OrganisationList, self).get_context_data(*args, **kwargs)
		context['section_menu'] = menu()

		serializer = self.serializer_class(self.object_list)

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
				'verbose_name': "type",
				# 'type': "string",
			},
			{
				'name': "sectors",
				# 'verbose_name': "sectors",
				'type': "list",
			},
			{
				'name': "country",
				# 'verbose_name': "home country",
				# 'type': "string",
			},
			{
				'name': "website",
				# 'verbose_name': "website",
				'type': "url",
			},
		]

		context['table'] = table_from_list(
			self.model,
			fields,
			serializer.data
		)

		if "form" not in context:
			context['form'] = OrganisationForm(**self.get_form_kwargs())

		context['breadcrumbs'] = [
			{
				'label': _("Organisations"),
			},
		]

		return context

	def get(self, request, *args, **kwargs):
		format = request.accepted_renderer.format
		method = kwargs.get('url_method', None)

		if format == 'html':
			self.object_list = self.get_filtered_queryset()
			context = self.get_context_data(object_list=self.object_list)

			if method == 'create':
				template_name = "form.html"
			else:
				template_name = "list.html"

			return Response(
				context,
				template_name=template_name,
			)

		return super(OrganisationList, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		format = request.accepted_renderer.format

		if format == 'html':
			form = OrganisationForm(**self.get_form_kwargs())

			if form.is_valid():
				self.object = form.save()
				return HttpResponseRedirect(self.get_success_url())

			self.object_list = self.get_filtered_queryset()
			context = self.get_context_data(
				object_list=self.object_list,
				form=form
			)

			return Response(
				context,
				template_name="form.html",
			)

		return super(OrganisationList, self).post(request, *args, **kwargs)


class OrganisationDetail(SimpleModelFormMixin, RetrieveUpdateDestroyAPIView):
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
		context['section_menu'] = menu()
		context['breadcrumbs'] = [
			{
				'label': _("Organisations"),
				'url': reverse('organisation-list')
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
			'organisation-detail',
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
						'organisation-detail',
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

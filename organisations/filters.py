import django_filters
from django import forms
from django.db.models import Q

from kapua.locations.models import Country

from .models import Organisation, OrganisationType
from unocha.models import Sector

from django.forms.widgets import SelectMultiple


class MultipleChoiceAndFilter(django_filters.MultipleChoiceFilter):
	"""
	This filter preforms an OR query on the selected options.
	"""
	field_class = forms.MultipleChoiceField

	def filter(self, qs, value):
		value = value or ()

		if len(value) == len(self.field.choices):
			return qs

		for v in value:
			qs = qs.filter(**{self.name: v})

		return qs.distinct()


class OrganisationFilter(django_filters.FilterSet):
	name = django_filters.CharFilter(
		lookup_type='icontains',
	)
	sectors = MultipleChoiceAndFilter()

	def __init__(self, *args, **kwargs):
		super(OrganisationFilter, self).__init__(*args, **kwargs)

		# Only show sectors referenced by organisations
		self.form.fields['sectors'].choices = Sector.objects.filter(
			organisation__in=Organisation.objects.all()
		).distinct().values_list('id', 'name')

		# Only show countries that have an organisation
		self.form.fields['country'].choices = Country.objects.filter(
			pk__in=Organisation.objects.values('country').distinct()
		).order_by('name').values_list('id', 'name')

		self.form.fields['country'].choices.insert(
			0, ("", self.form.fields['country'].empty_label)
		)

	class Meta:
		model = Organisation

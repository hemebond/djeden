import django_filters

from kapua.locations.models import Country

from .models import Organisation, OrganisationType


class OrganisationFilter(django_filters.FilterSet):
	name = django_filters.CharFilter(
		lookup_type='icontains'
	)
	country = django_filters.ModelMultipleChoiceFilter(
		queryset=Country.objects.order_by('name')
	)
	orgtype = django_filters.ModelMultipleChoiceFilter(
		queryset=OrganisationType.objects.all()
	)

	class Meta:
		model = Organisation
		fields = ['name', 'country', 'orgtype', 'sectors']

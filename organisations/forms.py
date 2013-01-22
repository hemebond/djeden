from django import forms
from .models import Organisation
from kapua.locations.models import Location, LocationType


class OrganisationForm(forms.ModelForm): 
	class Meta:
		model = Organisation
		exclude = ('offices',)

	def __init__(self, *args, **kwargs):
		super(OrganisationForm, self).__init__(*args, **kwargs)

		# self.fields['offices'].queryset = Location.objects.filter(
		# 	type=LocationType.objects.get(name="Office")
		# )

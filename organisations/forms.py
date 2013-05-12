from django import forms
from organisations.models import Organisation


class OrganisationForm(forms.ModelForm):
	class Meta:
		model = Organisation
		exclude = ('offices',)

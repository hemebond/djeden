from django.contrib import admin
from django import forms
from .models import Sector, Theme


class SectorForm(forms.ModelForm):
	class Meta:
		model = Sector
		widgets = {
			'themes': forms.CheckboxSelectMultiple,
		}


class SectorAdmin(admin.ModelAdmin):
	form = SectorForm


admin.site.register(Sector, SectorAdmin)
admin.site.register(Theme)

from django.contrib import admin
from .models import Organisation, OrganisationType
from .forms import OrganisationForm


class OrganisationAdmin(admin.ModelAdmin):
	form = OrganisationForm

admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(OrganisationType)

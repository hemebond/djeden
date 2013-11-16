from django.contrib import admin
from .models import Project, ProjectOrganisation, OrganisationRole, Task, Hazard

admin.site.register(Project)
admin.site.register(ProjectOrganisation)
admin.site.register(OrganisationRole)
admin.site.register(Task)
admin.site.register(Hazard)

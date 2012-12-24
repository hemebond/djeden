from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

#from tasks.models import Task
import tasks
from unocha.models import Sector, Theme
from organisations.models import Sector, Organisation


class Country(models.Model):
	name = models.CharField(max_length=64)

	def __unicode__(self):
		return u"%s" % self.name


class Currency(models.Model):
	"""
	The currency used by the project
	"""

	name = models.CharField(max_length=16)
	country = models.ForeignKey(Country)

	def __unicode__(self):
		return u"%s" % self.name


class Status(models.Model):
	"""
	Project status
	"""

	name = models.CharField(max_length=32)

	def __unicode__(self):
		return u"%s" % self.name


class Hazard(models.Model):
	name = models.CharField(max_length=64)

	def __unicode__(self):
		return u"%s" % self.name


class Hfa(models.Model):
	"""
	Hyogo Framework for Action (HFA)
	"""

	name = models.CharField(max_length=256)
	description = models.TextField()

	def __unicode__(self):
		return u"%s" % self.name


class Project(models.Model):
	name = models.CharField(max_length=128)
	code = models.CharField(max_length=32)
	description = models.TextField(blank=True)
	status = models.ForeignKey(Status)
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)
	currency = models.ForeignKey(Currency, blank=True, null=True)
	countries = models.ManyToManyField(Country, blank=True, null=True)
	hazards = models.ManyToManyField(Hazard, blank=True, null=True)
	hfas = models.ManyToManyField(Hfa, blank=True, null=True)

	# A sector has themes associated with it, and only those themes will
	# be available for a project
	sectors = models.ManyToManyField(Sector, blank=True, null=True)
	themes = models.ManyToManyField(Theme, blank=True, null=True)

	# Organisations supporting, funding or associated with a project
	organisations = models.ManyToManyField(
		Organisation,
		through='ProjectOrganisation',
		blank=True,
		null=True
	)

	def __unicode__(self):
		return u"%s" % self.name


class OrganisationRole(models.Model):
	name = models.CharField(max_length=32)

	def __unicode__(self):
		return u"%s" % self.name


class ProjectOrganisation(models.Model):
	project = models.ForeignKey(Project)
	organisation = models.ForeignKey(Organisation)
	role = models.ForeignKey(OrganisationRole)

	def __unicode__(self):
		return u"%s" % self.organisation.name


class Task(tasks.models.Task):
	# Tasks, activities and issues associated with this project
	project = models.ForeignKey(Project, related_name="tasks", blank=True, null=True)


class Contact(models.Model):
	"""
	An individual actively a part of a a relief effort.
	"""

	user = models.ForeignKey(User, related_name="projects")
	project = models.ForeignKey(Project, related_name="contacts")
	themes = models.ManyToManyField(Theme)

	def __unicode__(self):
		return u"%s" % self.user

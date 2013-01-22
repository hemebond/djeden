from django.db import models

from unocha.models import Sector

from kapua.locations.models import Country, Location


class OrganisationType(models.Model):
	"""
	The type of organisation.
	"""

	name = models.CharField(max_length=32)

	def __unicode__(self):
		return u"%s" % self.name


class Organisation(models.Model):
	"""
	A group actively engaged in relief efforts.
	"""

	name = models.CharField(
		max_length=128,
		help_text="The official name of the organisation. Preference should be given the English translation of the organisation.",
	)
	acronym = models.CharField(
		max_length=16,
		help_text="Acronym of the organisation.",
	)
	orgtype = models.ForeignKey(
		OrganisationType,
		verbose_name="type",
	)
	website = models.URLField(blank=True, null=True)
	sectors = models.ManyToManyField(Sector, blank=True, null=True)
	country = models.ForeignKey(
		Country,
		verbose_name="home country",
		blank=True,
		null=True,
		related_name="+",
	)
	offices = models.ManyToManyField(Location, blank=True, null=True)

	def __unicode__(self):
		return u"%s" % self.name

	class Meta:
		ordering = ('name',)

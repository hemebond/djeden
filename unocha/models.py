from django.db import models


class Theme(models.Model):
	"""
	Thematic Areas

	Theme of the project, e.g., drug abuse, conflict prevention, etc.
	Only themes application to the project sector are available.
	"""

	name = models.CharField(max_length=128)

	def __unicode__(self):
		return u"%s" % self.name

	class Meta:
		ordering = ['name',]


class Sector(models.Model):
	"""
	Area of support of the organisation. Also known as CAP sector or cluster.
	"""

	name = models.CharField(max_length=128)
	# Not all themes are applicable to all sectors
	themes = models.ManyToManyField(Theme, blank=True, null=True)

	def __unicode__(self):
		return u"%s" % self.name

	class Meta:
		ordering = ['name',]

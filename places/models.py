from django.contrib.gis.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Place(MPTTModel, models.Model):
	name = models.CharField(max_length=256)

	area = models.IntegerField()
	lon = models.FloatField()
	lat = models.FloatField()

	# MPTT parent field
	parent = TreeForeignKey(
		'self',
		null=True,
		blank=True,
		related_name='children',
	)

	class Meta:
		ordering = ('name',)

	# Returns the string representation of the model.
	def __unicode__(self):
		return u"%s" % self.name


class Country(Place):
	# pop2005 = models.IntegerField('Population 2005')
	fips = models.CharField('FIPS Code', max_length=2)
	iso2 = models.CharField('2 Digit ISO', max_length=2)
	iso3 = models.CharField('3 Digit ISO', max_length=3)
	un = models.IntegerField('United Nations Code')
	region = models.IntegerField('Region Code')
	subregion = models.IntegerField('Sub-Region Code')

	class Meta:
		ordering = ('name',)

	# GeoDjango-specific: a geometry field (MultiPolygonField), and
	# overriding the default manager with a GeoManager instance.
	# mpoly = models.MultiPolygonField()
	# objects = models.GeoManager()

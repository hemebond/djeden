from rest_framework import serializers
from organisations.models import Organisation, OrganisationType
from kapua.locations.models import Location


class OrganisationTypeSerializer(serializers.HyperlinkedModelSerializer):
	pk = serializers.Field()
	# __unicode__ = serializers.Field()

	class Meta:
		model = OrganisationType
		view_name = 'organisation-type-detail'


class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
	# orgtype = serializers.HyperlinkedRelatedField(view_name='organisation-type-detail')
	orgtype = serializers.Field()
	# orgtype = OrganisationTypeSerializer()
	pk = serializers.Field()
	country = serializers.Field()
	# __unicode__ = serializers.Field()
	sectors = serializers.ManyRelatedField()
	offices = serializers.ManyRelatedField()
	lat = serializers.SerializerMethodField("get_lat")
	lon = serializers.SerializerMethodField("get_lon")

	def get_lat(self, obj, *args, **kwargs):
		if obj.country is not None:
			return obj.country.lat
		return None

	def get_lon(self, obj, *args, **kwargs):
		if obj.country is not None:
			return obj.country.lon
		return None

	class Meta:
		model = Organisation
		depth = 1


class LocationSerializer(serializers.Serializer):
	pk = serializers.Field()
	name = serializers.Field()
	organisation = serializers.SerializerMethodField("get_organisation")
	country = serializers.SerializerMethodField("get_country")
	ancestors = serializers.SerializerMethodField("get_ancestors")
	type = serializers.Field(source="type.name")

	def get_organisation(self, obj, *args, **kwargs):
		return u"%s" % obj.organisation_set.all()[0]

	def get_country(self, obj, *args, **kwargs):
		qs = obj.get_root()
		return u"%s" % qs

	def get_ancestors(self, obj, *args, **kwargs):
		# print args
		# print kwargs
		# print obj
		qs = obj.get_ancestors()
		ancestors = []
		for idx, ancestor in enumerate(qs):
			ancestors.append(u"%s" % ancestor)
		return u", ".join(ancestors)

	class Meta:
		model = Location
		# fields = ('pk', 'name', 'ancestors')

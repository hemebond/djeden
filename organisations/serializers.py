from rest_framework import serializers
from .models import Organisation, OrganisationType


class OrganisationTypeSerializer(serializers.HyperlinkedModelSerializer):
	pk = serializers.Field()
	# __unicode__ = serializers.Field()

	class Meta:
		model = OrganisationType
		view_name = 'organisation_type_detail'


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
		view_name = 'organisation_detail'

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

	class Meta:
		model = Organisation
		depth = 1


class LocationSerializer(serializers.Serializer):
	pk = serializers.Field()
	name = serializers.Field()
	ancestors = serializers.SerializerMethodField("get_ancestors")
	type = serializers.Field(source="type.name")

	def get_ancestors(self, obj, *args, **kwargs):
		print args
		print kwargs
		print obj
		qs = obj.get_ancestors()
		ancestors = []
		for idx, ancestor in enumerate(qs):
			ancestors.append(u"%s" % ancestor)
		return u", ".join(ancestors)

	class Meta:
		model = Location
		# fields = ('pk', 'name', 'ancestors')

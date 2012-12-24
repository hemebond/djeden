from rest_framework import serializers
from organisations import models


class OrganisationTypeSerializer(serializers.HyperlinkedModelSerializer):
	pk = serializers.Field()
	# __unicode__ = serializers.Field()

	class Meta:
		model = models.OrganisationType
		view_name = 'organisation-type-detail'


class OrganisationSerializer(serializers.HyperlinkedModelSerializer):
	# orgtype = serializers.HyperlinkedRelatedField(view_name='organisation-type-detail')
	orgtype = serializers.Field()
	# orgtype = OrganisationTypeSerializer()
	pk = serializers.Field()
	country = serializers.Field()
	# __unicode__ = serializers.Field()
	sectors = serializers.ManyRelatedField()

	class Meta:
		model = models.Organisation
		depth = 1

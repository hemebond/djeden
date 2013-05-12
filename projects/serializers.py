from rest_framework import serializers
from .models import Project, ProjectOrganisation, Task


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
	pk = serializers.Field()
	status = serializers.Field(source='status')
	countries = serializers.ManyRelatedField()
	hazards = serializers.ManyRelatedField()
	hfas = serializers.ManyRelatedField()
	sectors = serializers.ManyRelatedField()
	themes = serializers.ManyRelatedField()
	organisations = serializers.HyperlinkedRelatedField(many=True, view_name="organisation_detail")

	# start_date = serializers.DateTimeField()
	# end_date = serializers.DateTimeField()

	class Meta:
		model = Project
		# fields = ('url', 'pk', 'name', 'status')
		view_name = 'project_detail'


class ProjectOrganisationSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProjectOrganisation
		view_name = "organisation_detail"


class TaskSerializer(serializers.ModelSerializer):
	pk = serializers.Field()
	project = serializers.Field()
	task_type = serializers.ChoiceField(choices=Task.TYPES)
	priority = serializers.ChoiceField(choices=Task.PRIORITIES)
	severity = serializers.ChoiceField(choices=Task.SEVERITIES)
	resolution = serializers.ChoiceField(choices=Task.RESOLUTIONS)

	class Meta:
		model = Task
		#fields = ('pk', 'name')
		view_name = 'project_task_detail'

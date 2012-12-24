from rest_framework import serializers
from .models import Project, Task


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
	pk = serializers.Field()
	status = serializers.Field(source='status')

	class Meta:
		model = Project
		fields = ('url', 'pk', 'name', 'status')


class TaskSerializer(serializers.HyperlinkedModelSerializer):
	#pk = serializers.Field()
	project = serializers.Field()

	class Meta:
		model = Task
		#fields = ('pk', 'name')

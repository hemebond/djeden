from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.HyperlinkedModelSerializer):
	pk = serializers.Field()

	class Meta:
		model = Task
		fields = (
			'url',
			'pk',
			#'action',
			'created',
			#'dependencies',
			'description',
			'modified',
			'name',
			'priority',
			#'resolution',
			'severity',
			#'task',
			'task_type',
		)

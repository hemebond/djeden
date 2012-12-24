"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

# from projects.utils import DataTable
from projects.models import Project, Status


class DataTableTest(TestCase):

	def setUp(self):
		status = Status.objects.create(name="Started")
		self.project = Project.objects.create(
			name="My Project",
			code="MP",
			status=status,
		)

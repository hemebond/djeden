"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest
from django.test import TestCase

from organisations.models import Organisation
from organisations.filters import OrganisationFilter
from organisations.utils import DataTable


class DataTableTest(TestCase):

	def setUp(self):
		pass

	def test_datatable(self):
		"""
		Test to make sure we get back the correct structure and options.
		"""

		table = DataTable(
			fields=[
				'name',
				'description',
			],
			object_list=[
				{
					'name': "My Object",
					'description': "An object",
				},
			],
		)

		columns = [
			{
				'field': "name",
				'label': "Name",
			},
			{
				'field': "description",
				'label': "Description",
			},
		]
		rows = [
			{
				'name': "My Object",
				'description': "An object",
			},
		]

		self.assertEqual(table.columns, columns)
		self.assertEqual(table.rows, rows)


class FilterTest(TestCase):
	fixtures = ['/home/james/Workspace/django-eden/djeden/sample_organisations.json',]

	def setUp(self):
		pass

	def test_filterset(self):
		org = Organisation.objects.get(pk=2)

		f = OrganisationFilter(
			{'sectors': [5, 12]},
			Organisation.objects.all()
		)

		self.assertQuerysetEqual(f.qs, [org.pk], lambda o: o.pk)

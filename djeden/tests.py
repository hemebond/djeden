from django.utils import unittest

from djeden.utils import table_from_qs, table_from_list

from organisations.models import Organisation, OrganisationType


class DjangoUtilsTestCase(unittest.TestCase):
	maxDiff = None

	def test_table_from_list(self):
		serialized_data = [
			{
				'pk': 1,
				'url': '/organisations/2/',
				'name': u'Test Org',
				'orgtype': u'Test Org Type',
				'country': u'Afghanistan',
				'sectors': [
					u'Agriculture',
					u'Coordination and Support Services'
				],
				'offices': [],
				'lat': 33.677,
				'lon': 65.216,
				'acronym': u'ARCS',
				'website': u'http://www.arcs.org.af/'
			}
		]

		result = {
			'cols': [
				{
					'field': "name",
					'type': "CharField",
					'label': u"name",
				},
				{
					'field': "orgtype",
					'type': "ForeignKey",
					'label': u"type",
				},
				{
					'field': "sectors",
					'type': "ManyToManyField",
					'label': u"sectors",
				}
			],
			'rows': [
				{
					'pk': 1,
					'cells': [
						{
							'field': "name",
							'type': "CharField",
							'value': u"Test Org",
						},
						{
							'field': "orgtype",
							'type': "ForeignKey",
							'value': u"Test Org Type",
						},
						{
							'field': "sectors",
							'type': "ManyToManyField",
							'value': [
								u'Agriculture',
								u'Coordination and Support Services'
							],
						}
					]
				}
			]
		}

		self.assertEqual(
			table_from_list(
				serialized_data,
				Organisation,
				[
					"name",
					"orgtype",
					"sectors",
				]
			),
			result
		)

	def test_table_from_qs(self):
		orgtype = OrganisationType.objects.create(
			name="Test Org Type"
		)

		organisation = Organisation.objects.create(
			name="Test Org",
			orgtype=orgtype,
		)

		result = {
			'cols': [
				{
					'field': "name",
					'type': "CharField",
					'label': u"name",
				},
				{
					'field': "orgtype",
					'type': "ForeignKey",
					'label': u"type",
				},
				{
					'field': "sectors",
					'type': "ManyToManyField",
					'label': u"sectors",
				}
			],
			'rows': [
				{
					'pk': organisation.pk,
					'cells': [
						{
							'field': "name",
							'type': "CharField",
							'value': u"Test Org",
						},
						{
							'field': "orgtype",
							'type': "ForeignKey",
							'value': orgtype,
						},
						{
							'field': "sectors",
							'type': "ManyToManyField",
							'value': [],
						}
					]
				}
			]
		}

		self.assertEqual(
			table_from_qs(
				Organisation.objects.filter(name="Test Org"),
				[
					"name",
					"orgtype",
					"sectors",
				]
			),
			result
		)

		organisation.delete()
		orgtype.delete()

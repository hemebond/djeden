import json
import re

from django.db.models.fields import FieldDoesNotExist
from django.contrib.admin.util import label_for_field


def table_from_list(object_list, model, field_list=[]):
	"""
		object_list is serialized data
	"""

	if not field_list and object_list:
		# field_list = model._meta.get_all_field_names()
		field_list = object_list[0].keys()

	table = {
		'cols': [],
		'rows': [],
	}

	is_first_object = True

	for o in object_list:
		row = {
			'pk': o['pk'],
			'cells': [],
		}

		for field_name in field_list:
			# FIXME: fields might be dicts
			if isinstance(field_name, dict):
				field_name = field_name['name']

			# Get value from object dict
			field_value = o[field_name]

			# Get label from verbose name
			try:
				field_vname = label_for_field(field_name, model)
			except AttributeError:
				field_vname = field_name

			# A field might not be a model field
			try:
				field = model._meta.get_field(field_name)

				# Get field type
				field_type = str(
					re.search(r"(\w+)'>$", str(field.__class__)).group(1)
				)
			except FieldDoesNotExist:
				if isinstance(field_value, list):
					field_type = "ManyToManyField"
				else:
					field_type = ""

			if is_first_object:
				table['cols'].append({
					'field': field_name,
					'type': field_type,
					'label': field_vname,
				})

			row['cells'].append({
				'field': field_name,
				'type': field_type,
				'value': field_value,
			})

		if o['url']:
			row['cells'][0]['url'] = o['url']

		table['rows'].append(row)

		is_first_object = False

	return table


def detail_from_dict(model, data, field_list=None):
	"""
	data is serializer.data
	"""

	detail = []

	if not field_list:
		field_list = data.keys()

	for field in field_list:
		try:
			label = model._meta.get_field(field).verbose_name
		except FieldDoesNotExist:
			label = field

		value = data[field]

		if isinstance(value, list):
			field_type = "list"
		else:
			field_type = "string"

		detail.append({
			'field': field,
			'label': label,
			'value': value,
			'type': field_type,
		})

	return detail


def table_from_qs(queryset, field_list=[]):
	"""
		Takes a queryset (object_list) and produces a table object.
	"""

	model = queryset.model

	# Temporary fix for dict fields
	if not field_list:
		field_list = model._meta.get_all_field_names()

	table = {
		'cols': [],
		'rows': [],
	}

	is_first_object = True

	for o in queryset:
		row = {
			'pk': o.pk,
			'cells': [],
		}

		for field_name in field_list:
			# FIXME: fields might be dicts
			if isinstance(field_name, dict):
				field_name = field_name['name']

			field = model._meta.get_field(field_name)

			# Get field type
			field_type = str(
				re.search(r"(\w+)'>$", str(field.__class__)).group(1)
			)

			if field_type == "ManyToManyField":
				field_value = [unicode(obj) for obj in getattr(o, field_name).all()]
			else:
				field_value = getattr(o, field_name)

			if is_first_object:
				table['cols'].append({
					'field': field_name,
					'type': field_type,
					'label': unicode(field.verbose_name),
				})

			row['cells'].append({
				'field': field_name,
				'type': field_type,
				'value': field_value,
			})

		table['rows'].append(row)

		is_first_object = False

	return table


class JSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if hasattr(obj, 'isoformat'):  # handles both date and datetime objects
			return obj.isoformat()
		else:
			return json.JSONEncoder.default(self, obj)

import json
import re

from django.db.models import fields


def table_from_list(object_list, model, field_list=[]):
	"""
		object_list is serialized data
	"""

	if not field_list:
		field_list = model._meta.get_all_field_names()

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

			# A field might not be a model field
			try:
				field = model._meta.get_field(field_name)

				# Get label from verbose name
				field_vname = unicode(field.verbose_name)

				# Get field type
				field_type = str(
					re.search(r"(\w+)'>$", str(field.__class__)).group(1)
				)
			except fields.FieldDoesNotExist:
				field_vname = field_name

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
		except fields.FieldDoesNotExist:
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





# def table_from_qs(queryset, field_list=[], display_link=[]):
# 	if not field_list:
# 		field_list = queryset.model._meta.get_all_field_names()

# 	# Temporarily convert from dict to list
# 	# field_list = [field['name'] for field in field_list]

# 	table = {
# 		'cols': [],
# 		'rows': [],
# 	}

# 	for idx, field in enumerate(field_list):
# 		if type(field) == dict:
# 			field = field['name']

# 		try:
# 			label = label_for_field(field, queryset.model)
# 		except FieldDoesNotExist:
# 			label = field

# 		model_field = queryset.model._meta.get_field(field)

# 		if model_field.rel and isinstance(model_field, fields.related.ManyToManyField):
# 			field_type = "list"
# 		elif isinstance(model_field, fields.EmailField):
# 			field_type = "email"
# 		else:
# 			field_type = "str"

# 		table['cols'].append({
# 			'field': field,
# 			'type': field_type,
# 			'label': unicode(label),
# 		})

# 	for obj in queryset:
# 		row = {
# 			'pk': obj.pk,
# 			'cells': [],
# 		}

# 		for idx, field in enumerate(field_list):
# 			# Temporary transition fix
# 			if isinstance(field, dict):
# 				field = field['name']

# 			cell = {
# 				'field': field,
# 				'type': table['cols'][idx]['type'],
# 				'value': unicode(getattr(obj, field)),
# 			}

# 			if col[idx]['type'] == 'list':


# 			if "name" == field and hasattr(obj, "url"):
# 				cell.update({'url': getattr(obj, 'url')})

# 			row['cells'].append(cell)

# 		table['rows'].append(row)

# 	return table


class JSONEncoder(json.JSONEncoder):
	def default(self, obj):
		if hasattr(obj, 'isoformat'):  # handles both date and datetime objects
			return obj.isoformat()
		else:
			return json.JSONEncoder.default(self, obj)

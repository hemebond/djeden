from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def vartype(variable):
	return type(variable)


@register.filter
def keyvalue(d, key):
	# {{ dictionary|keyvalue:key_variable }}
    return d.getattr(key)


@register.filter
def value_for(obj, field):
	value = ""

	if obj:
		try:
			value = getattr(obj, field)
		except AttributeError:
			value = obj.get(field)

	if hasattr(value, "all") and hasattr(value.all, '__call__'):
		value = value.all()

	return value


class TableNode(template.Node):
	def __init__(self, object_list):
		self.object_list = object_list

	def render(self, context):
		# Match the object_list variable name against the actual
		# context property
		object_list = self.object_list.resolve(context)

		t = template.loader.get_template("_table.html")

		table = {
			'labels': []
		}

		for f in object_list.queryset.fields:
			label = object_list.queryset \
			             .model \
			             ._meta \
			             .get_field(f) \
			             .verbose_name
			table.labels.append(label)

		context.update({'table': table})
		return t.render(context)
		# return mark_safe("<p><i>%s</i></p>" % self.bits)


@register.tag
def table(parser, token):
	bits = token.split_contents()[1:]
	object_list = parser.compile_filter(bits[0])
	return TableNode(object_list)

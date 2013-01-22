from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def v(record, field):
	if record:
		try:
			return getattr(record, field['name'])
		except AttributeError:
			pass

		return record.get(field['name'])

	return ""


class TableNode(template.Node):
	def __init__(self, table):
		self.table = table

	def render(self, context):
		# Match the table variable name against the actual
		# context property
		table = self.table.resolve(context)

		t = template.loader.get_template("_table.html")

		print dir(table)
		table.labels = []
		for f in table.fields:
			label = table.queryset \
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
	table = parser.compile_filter(bits[0])
	return TableNode(table)
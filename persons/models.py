from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class Person(models.Model):
	user_account = models.ForeignKey(User)

	first_name = models.CharField(
		max_length=64
	)
	middle_name = models.CharField(
		max_length=64,
		blank=True,
		null=True
	)
	last_name = models.CharField(
		max_length=64,
		blank=True,
		null=True
	)
	initials = models.CharField(
		max_length=8,
		blank=True,
		null=True
	)

	preferred_name = models.CharField(
		max_length=64,
		blank=True,
		null=True
	)
	local_name = models.CharField(
		max_length=64,
		blank=True,
		null=True,
		help_text=_("Name of the person in local language and script")
	)

	label = models.CharField(
		max_length=64,
		blank=True,
		null=True,
		help_text=_("ID tag number or label")
	)

	GENDER_OPTIONS = [
		(1, _("Male")),
		(2, _("Female")),
	]
	gender = models.IntegerField(
		choices=GENDER_OPTIONS,
		blank=True,
		null=True
	)

	date_of_birth = models.DateField(
		blank=True,
		null=True
	)
	AGE_GROUP_OPTIONS = [
		(1, _("Infant (0-1)")),
		(2, _("Child (2-11)")),
		(3, _("Adolescent (12-20)")),
		(4, _("Adult (21-50)")),
		(5, _("Senior (50+)"))
	]
	age_group = models.IntegerField(
		choices=AGE_GROUP_OPTIONS,
		blank=True,
		null=True
	)

import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class Task(models.Model):
	name = models.CharField(max_length=64)
	description = models.TextField(blank=True)

	TYPES = (
		(0, _("Task")),
		(1, _("New Feature")),
		(2, _("Defect")),
		(3, _("Improvement")),
	)
	task_type = models.IntegerField(
		choices=TYPES,
		default=0,
	)

	PRIORITIES = (
		(0, _("Critical")),
		(1, _("Urgent")),
		(2, _("High")),
		(3, _("Normal")),
		(4, _("Low")),
		(5, _("Lowest")),
	)
	priority = models.IntegerField(
		choices=PRIORITIES,
		default=3,
	)

	SEVERITIES = (
		(0, _("Blocker")),
		(1, _("Critical")),
		(2, _("Major")),
		(3, _("Normal")),
		(4, _("Minor")),
		(5, _("Trivial")),
	)
	severity = models.IntegerField(
		choices=SEVERITIES,
		default=3,
	)

	RESOLUTIONS = (
		(0, _("Open")),
		(1, _("Closed")),
		(2, _("Won't fix")),
		(3, _("Invalid")),
		(4, _("Duplicate")),
	)
	resolution = models.IntegerField(
		choices=RESOLUTIONS,
		default=0,
	)

	dependencies = models.ManyToManyField(
		'self',
		related_name="+",
		symmetrical=False,
		blank=True,
		null=True,
	)
	created = models.DateTimeField(
		auto_now_add=True,
		editable=False,
	)
	modified = models.DateTimeField(
		auto_now=True,
		editable=False,
	)

	def __unicode__(self):
		return u"%s" % self.name


class TaskUser(models.Model):
	user = models.ForeignKey(User)
	task = models.ForeignKey(Task)
	assigned = models.BooleanField(
		default=False,
	)


class Action(models.Model):
	author = models.ForeignKey(User)
	task = models.ForeignKey(Task)
	comment = models.TextField(
		blank=True,
	)
	start = models.DateTimeField(
		default=datetime.datetime.now,
	)

	def __unicode__(self):
		return "%s - %s" % (
			self.author,
			self.date,
		)

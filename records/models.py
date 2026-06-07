from django.conf import settings
from django.db import models


class AuditLog(models.Model):
	ACTION_CHOICES = [
		("CREATE", "Create"),
		("UPDATE", "Update"),
		("DELETE", "Delete"),
	]

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
	)
	action = models.CharField(max_length=10, choices=ACTION_CHOICES)
	app_label = models.CharField(max_length=100)
	model_name = models.CharField(max_length=100)
	object_pk = models.CharField(max_length=200, blank=True, null=True)
	object_repr = models.TextField(blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	extra = models.JSONField(null=True, blank=True)

	class Meta:
		ordering = ["-timestamp"]

	def __str__(self) -> str:
		return f"{self.timestamp.isoformat()} {self.app_label}.{self.model_name} {self.action}"

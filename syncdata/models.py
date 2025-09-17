from django.db import models


class SyncedFile(models.Model):
	name = models.CharField(max_length=255)
	size = models.BigIntegerField()
	file_type = models.CharField(max_length=50)
	deal_id = models.CharField(max_length=100)
	crm_source = models.CharField(max_length=50)
	sync_timestamp = models.DateTimeField(auto_now_add=True)
	file_id = models.CharField(max_length=255, unique=True)  # CRM file ID
	file_name = models.CharField(max_length=255)
	properties = models.JSONField(null=True, blank=True)
	file_url = models.TextField(null=True, blank=True)

	class Meta:
		indexes = [
			models.Index(fields=['deal_id', 'crm_source', 'size']),
		]
	
	def __str__(self):
		return f"{self.name} ({self.file_type})"

# Create your models here.

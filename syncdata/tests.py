from django.test import TestCase
from .models import SyncedFile


class SyncedFileTest(TestCase):
	def test_create_file(self):
		file = SyncedFile.objects.create(
			name="test.pdf", size=1234, file_type="pdf",
			deal_id="123", crm_source="hubspot", file_id="abc"
		)
		self.assertEqual(file.name, "test.pdf")

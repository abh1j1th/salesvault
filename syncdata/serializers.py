from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from syncdata.models import SyncedFile


class SyncedFileSerializer(ModelSerializer):
    class Meta:
        model = SyncedFile
        fields = '__all__'
        # read_only_fields = ['sync_timestamp']
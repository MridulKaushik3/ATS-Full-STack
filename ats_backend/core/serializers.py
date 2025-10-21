from rest_framework import serializers
from .models import ResumeRecord

class ResumeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeRecord
        fields = '__all__'

from django.db import models

# Create your models here.

class ResumeRecord(models.Model):
    job_description = models.TextField()
    resume_file = models.FileField(upload_to='resumes/')
    score = models.IntegerField()
    keywords_missing = models.TextField(blank=True)
    final_thoughts = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

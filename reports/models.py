from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('can_view_report', 'Can view report'),
            ('edit_report', 'Can edit report'),  
            ('can_delete_report', 'Can delete report'),  
        )

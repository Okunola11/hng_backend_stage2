from django.db import models
from users.models import User

class Organisation(models.Model):
    org_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(User, related_name='organisations')

    def __str__(self):
        return self.name

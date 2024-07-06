from django.conf import settings
from django.db import models

class Organisation(models.Model):
    orgId = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Membership', related_name='organisation_members')
    
    def __str__(self):
        return self.name

class Membership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='membership_user')  
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='membership_organisation')  

    class Meta:
        unique_together = (('user', 'organisation'),)  

    def __str__(self):
        return f"{self.user.email} - {self.organisation.name}"

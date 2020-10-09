from django.db import models

# Create your models here.
class Profile(models.Model):
    content = models.TextField()
    # image
    # location
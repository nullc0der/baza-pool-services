from django.db import models

from versatileimagefield.fields import VersatileImageField

# Create your models here.


class Token(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=30)
    logo = VersatileImageField(upload_to='tokenlogos/')
    homepage_url = models.URLField()
    algo = models.CharField(max_length=30)
    is_archived = models.BooleanField(default=False)
    has_won = models.BooleanField(default=False)
    added_date = models.DateField(null=True, auto_now_add=True)
    won_date = models.DateField(null=True)

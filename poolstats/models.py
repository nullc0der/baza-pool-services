from django.db import models

# Create your models here.


class PoolInfo(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=40)
    logo_url = models.URLField()
    pool_url = models.URLField()
    pool_stats_api_url = models.URLField()

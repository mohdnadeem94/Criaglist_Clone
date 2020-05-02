from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now = True)
    minimum_price = models.CharField(max_length=10)
    maximum_price = models.CharField(max_length=10)
    city_name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Searches'

    def __str__(self):
        return self.search

from django.db import models

class Observation(models.Model):
    observation_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    country_code = models.CharField(max_length=10)
    city_name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=12, decimal_places=6)
    longitude = models.DecimalField(max_digits=12, decimal_places=6)
    wind_speed = models.DecimalField(max_digits=12, decimal_places=6)
    wind_direction_short = models.CharField(max_length=10)
    wind_direction_full = models.CharField(max_length=200)
    wind_direction_degrees = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        unique_together = ('latitude', 'longitude')

class APItoken(models.Model):
    token = models.CharField(max_length=32)

class ElementsReturned(models.Model):
    elements = models.IntegerField(default=10)

class Localization(models.Model):
    city_name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=12, decimal_places=6)
    longitude = models.DecimalField(max_digits=12, decimal_places=6)
    country = models.CharField(max_length=200)
    country_code = models.CharField(max_length=10)
    capital = models.CharField(max_length=50)

    class Meta:
        unique_together = ('city_name', 'latitude', 'longitude', 'country', 'country_code', 'capital')

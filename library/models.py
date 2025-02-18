from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Library(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, unique=True)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Library"
        verbose_name_plural = "Libraries"
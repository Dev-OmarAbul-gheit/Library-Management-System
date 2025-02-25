from django.contrib.gis.geos import Point
from django_filters import rest_framework
from rest_framework.serializers import ValidationError
from .models import Library


class LibraryFilter(rest_framework.FilterSet):
    coordinates = rest_framework.CharFilter(method="filter_by_distance")

    def filter_by_distance(self, queryset, name, value):
        longitude, latitude = map(float, value.split(","))
        if not (-90 <= latitude <= 90):
            raise ValidationError("Latitude must be between -90 and 90 degrees.")
        if not (-180 <= longitude <= 180):
            raise ValidationError("Longitude must be between -180 and 180 degrees.")
        return queryset.annotate_distance(Point(longitude, latitude, srid=4326))

    class Meta:
        model = Library
        fields = ["id", "books__category", "books__author"]

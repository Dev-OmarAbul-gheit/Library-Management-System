from rest_framework import serializers
from .models import Library
import re


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'name', 'location', 'coordinates'] # "coordinates": "POINT (longitude latitude)"
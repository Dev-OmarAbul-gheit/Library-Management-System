from django.db.models import QuerySet
from django.db.models.functions import Round
from django.contrib.gis.db.models.functions import Distance


class LibraryQuerySet(QuerySet):
    def annotate_distance(self, location):
        return self.annotate(
            distance=Round(Distance("coordinates", location) / 1000, precision=2)
        ).order_by("distance")

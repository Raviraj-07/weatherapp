from pyexpat import model
from django.db import models
from django.utils import timezone


class TimeStamped(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField()
    updated = models.DateTimeField()

    def save(self, *args, **kwargs) -> None:
        _now = timezone.now()
        self.updated = _now
        if not self.id:
            self.created = _now
        return super(TimeStamped, self).save( *args, **kwargs)
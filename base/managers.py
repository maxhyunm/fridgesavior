from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return
        SoftDeleteQuerySet(self.Model).filter(deleted_at=None)
        return SoftDeleteQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeleteQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeleteQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeleteQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)
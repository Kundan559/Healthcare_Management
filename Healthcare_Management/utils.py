from django.db import models


class ActiveQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def delete(self):
        return self.update(is_active=False)


class ActiveManager(models.Manager):
    def get_queryset(self):
        return ActiveQuerySet(self.model, using=self._db).filter(is_active=True)


class AllObjectsManager(models.Manager):
    pass

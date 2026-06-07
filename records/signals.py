import datetime
import json
import logging

from django.db import connection
from django.db.models.signals import post_delete, post_save, pre_delete
from django.db.utils import OperationalError, ProgrammingError
from django.dispatch import receiver
from django.forms.models import model_to_dict

from .models import AuditLog
from .middleware import get_current_user

logger = logging.getLogger(__name__)


def _safe_repr(instance):
    try:
        return str(instance)
    except Exception:
        return repr(instance)


def _audit_table_exists():
    try:
        return AuditLog._meta.db_table in connection.introspection.table_names()
    except (OperationalError, ProgrammingError):
        return False


def _serialize_instance(instance):
    try:
        raw = model_to_dict(instance)
    except Exception:
        return None

    extra = {}
    for key, value in raw.items():
        if isinstance(value, (datetime.datetime, datetime.date)):
            extra[key] = value.isoformat()
        else:
            try:
                json.dumps(value)
                extra[key] = value
            except Exception:
                extra[key] = str(value)

    return extra


@receiver(post_save)
def model_post_save(sender, instance, created, **kwargs):
    if sender.__name__ == "AuditLog" or getattr(sender._meta, "abstract", False):
        return

    if not _audit_table_exists():
        return

    user = get_current_user()
    if not user or not user.is_authenticated:
        user = None
        
    action = "CREATE" if created else "UPDATE"
    extra = _serialize_instance(instance)

    try:
        AuditLog.objects.create(
            user=user,
            action=action,
            app_label=sender._meta.app_label,
            model_name=sender.__name__,
            object_pk=str(getattr(instance, "pk", "")),
            object_repr=_safe_repr(instance),
            extra=extra,
        )
    except Exception:
        logger.exception("Failed to create audit log for %s", sender.__name__)


@receiver(pre_delete)
def model_pre_delete(sender, instance, **kwargs):
    if sender.__name__ == "AuditLog" or getattr(sender._meta, "abstract", False):
        return

    setattr(instance, "_audit_log_pk", getattr(instance, "pk", None))


@receiver(post_delete)
def model_post_delete(sender, instance, **kwargs):
    if sender.__name__ == "AuditLog" or getattr(sender._meta, "abstract", False):
        return

    if not _audit_table_exists():
        return

    user = get_current_user()
    object_pk = getattr(instance, "_audit_log_pk", getattr(instance, "pk", ""))

    try:
        AuditLog.objects.create(
            user=user,
            action="DELETE",
            app_label=sender._meta.app_label,
            model_name=sender.__name__,
            object_pk=str(object_pk),
            object_repr=_safe_repr(instance),
            extra=None,
        )
    except Exception:
        logger.exception("Failed to create audit log for %s delete", sender.__name__)

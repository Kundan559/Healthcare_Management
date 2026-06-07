from .models import UserRole


def get_user_role(user):
    if not user.is_authenticated:
        return None

    if user.is_superuser:
        return 'SUPERUSER'

    try:
        return user.userrole.role
    except UserRole.DoesNotExist:
        return None

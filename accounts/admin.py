from Healthcare_Management.admin import admin_site, RoleBasedModelAdmin, export_as_csv_action
from .models import UserRole


class UserRoleAdmin(RoleBasedModelAdmin):
    allowed_roles = ['ADMIN']
    change_roles = ['ADMIN']
    add_roles = ['ADMIN']
    delete_roles = ['ADMIN']

    list_display = ('user', 'role')
    search_fields = ('user__username', 'role')
    actions = [export_as_csv_action('Export selected user roles as CSV')]


admin_site.register(UserRole, UserRoleAdmin)

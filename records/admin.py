from Healthcare_Management.admin import admin_site, RoleBasedModelAdmin, export_as_csv_action, export_as_pdf_action
from .models import AuditLog


class AuditLogAdmin(RoleBasedModelAdmin):
    allowed_roles = ['ADMIN']
    view_roles = ['ADMIN']
    add_roles = []
    change_roles = []
    delete_roles = []

    list_display = ("timestamp", "user", "action", "app_label", "model_name", "object_pk")
    list_filter = ("action", "app_label", "model_name", "user")
    search_fields = ("object_repr", "object_pk", "user__username")
    readonly_fields = ("timestamp", "user", "action", "app_label", "model_name", "object_pk", "object_repr", "extra")
    date_hierarchy = 'timestamp'
    actions = [
        export_as_csv_action('Export selected audit logs as CSV'),
        export_as_pdf_action('Export selected audit logs as PDF'),
    ]


admin_site.register(AuditLog, AuditLogAdmin)

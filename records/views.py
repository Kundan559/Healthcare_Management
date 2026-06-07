from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import AuditLog


def staff_required(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required(login_url='login')
@user_passes_test(staff_required)
def audit_log_list(request):
    logs = AuditLog.objects.all().order_by('-timestamp')

    query = request.GET.get('q', '').strip()
    action = request.GET.get('action', '').strip()
    app_label = request.GET.get('app_label', '').strip()
    model_name = request.GET.get('model_name', '').strip()

    if query:
        logs = logs.filter(object_repr__icontains=query)
    if action:
        logs = logs.filter(action=action)
    if app_label:
        logs = logs.filter(app_label__icontains=app_label)
    if model_name:
        logs = logs.filter(model_name__icontains=model_name)

    paginator = Paginator(logs, 25)
    page_number = request.GET.get('page')
    audit_logs = paginator.get_page(page_number)

    return render(request, 'records/audit_log_list.html', {
        'audit_logs': audit_logs,
        'filters': {
            'q': query,
            'action': action,
            'app_label': app_label,
            'model_name': model_name,
        },
    })

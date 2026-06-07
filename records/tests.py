from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from .middleware import CurrentUserMiddleware
from .models import AuditLog
from patients.models import Patient

User = get_user_model()


class AuditLogTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="pass")
        self.factory = RequestFactory()

    def test_create_patient_generates_audit_log(self):
        request = self.factory.get("/")
        request.user = self.user

        def get_response(req):
            Patient.objects.create(
                name="John Doe",
                age=30,
                gender="Male",
                phone="1234567890",
                address="123 Main St",
            )
            return HttpResponse()

        middleware = CurrentUserMiddleware(get_response)
        middleware(request)

        patient_logs = AuditLog.objects.filter(action="CREATE", model_name="Patient")
        self.assertEqual(patient_logs.count(), 1)
        audit_log = patient_logs.first()
        self.assertEqual(audit_log.user, self.user)
        self.assertEqual(audit_log.action, "CREATE")
        self.assertEqual(audit_log.app_label, "patients")
        self.assertEqual(audit_log.model_name, "Patient")
        self.assertIn("John Doe", audit_log.object_repr)

    def test_delete_patient_generates_audit_log(self):
        patient = Patient.objects.create(
            name="Jane Doe",
            age=28,
            gender="Female",
            phone="0987654321",
            address="456 Elm St",
        )
        patient_pk = patient.pk

        request = self.factory.get("/")
        request.user = self.user

        def get_response(req):
            patient.delete()
            return HttpResponse()

        middleware = CurrentUserMiddleware(get_response)
        middleware(request)

        self.assertTrue(
            AuditLog.objects.filter(action="DELETE", model_name="Patient").exists()
        )
        audit_log = AuditLog.objects.filter(action="DELETE", model_name="Patient").first()
        self.assertEqual(audit_log.user, self.user)
        self.assertEqual(audit_log.app_label, "patients")
        self.assertEqual(audit_log.model_name, "Patient")
        self.assertEqual(audit_log.object_pk, str(patient_pk))

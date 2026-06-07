from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Patient
from accounts.models import UserRole
from django.urls import reverse


class PatientAjaxTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='admin', password='pass')
		UserRole.objects.create(user=self.user, role='ADMIN')
		self.patient = Patient.objects.create(name='Jane Doe', age=28, gender='Female', phone='111', address='Nowhere')

	def test_delete_and_restore_patient_ajax(self):
		login = self.client.login(username='admin', password='pass')
		self.assertTrue(login)
		del_url = reverse('delete_patient_ajax', args=[self.patient.id])
		resp = self.client.post(del_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertTrue(data.get('success'))
		self.patient.refresh_from_db()
		self.assertFalse(self.patient.is_active)

		# restore
		res_url = reverse('restore_patient_ajax', args=[self.patient.id])
		resp2 = self.client.post(res_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(resp2.status_code, 200)
		data2 = resp2.json()
		self.assertTrue(data2.get('success'))
		self.patient.refresh_from_db()
		self.assertTrue(self.patient.is_active)

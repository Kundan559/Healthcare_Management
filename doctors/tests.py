from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Doctor
from accounts.models import UserRole
from django.urls import reverse


class DoctorAjaxTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='admin', password='pass')
		UserRole.objects.create(user=self.user, role='ADMIN')
		self.doctor = Doctor.objects.create(name='Dr Test', specialization='Cardiology', phone='000')

	def test_delete_and_restore_doctor_ajax(self):
		login = self.client.login(username='admin', password='pass')
		self.assertTrue(login)
		del_url = reverse('delete_doctor_ajax', args=[self.doctor.id])
		resp = self.client.post(del_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertTrue(data.get('success'))
		self.doctor.refresh_from_db()
		self.assertFalse(self.doctor.is_active)

		# restore
		res_url = reverse('restore_doctor_ajax', args=[self.doctor.id])
		resp2 = self.client.post(res_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(resp2.status_code, 200)
		data2 = resp2.json()
		self.assertTrue(data2.get('success'))
		self.doctor.refresh_from_db()
		self.assertTrue(self.doctor.is_active)

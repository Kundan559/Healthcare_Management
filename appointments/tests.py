from django.test import TestCase, Client
from django.contrib.auth.models import User
from patients.models import Patient
from doctors.models import Doctor
from .models import Appointment
from accounts.models import UserRole
from django.urls import reverse
from datetime import date, time


class AppointmentAjaxTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='admin', password='pass')
		UserRole.objects.create(user=self.user, role='ADMIN')
		self.patient = Patient.objects.create(name='John Doe', age=30, gender='Male', phone='12345', address='Somewhere')
		self.doctor = Doctor.objects.create(name='Dr Who', specialization='General', phone='54321')
		self.appointment = Appointment.objects.create(
			patient=self.patient,
			doctor=self.doctor,
			appointment_date=date.today(),
			appointment_time=time(hour=9, minute=0),
			status='PENDING'
		)

	def test_confirm_appointment_ajax(self):
		login = self.client.login(username='admin', password='pass')
		self.assertTrue(login)
		url = reverse('confirm_appointment_ajax', args=[self.appointment.id])
		response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertTrue(data.get('success'))
		self.appointment.refresh_from_db()
		self.assertEqual(self.appointment.status, 'CONFIRMED')

	def test_delete_and_restore_appointment_ajax(self):
		login = self.client.login(username='admin', password='pass')
		self.assertTrue(login)
		del_url = reverse('delete_appointment_ajax', args=[self.appointment.id])
		resp = self.client.post(del_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertTrue(data.get('success'))
		self.appointment.refresh_from_db()
		self.assertFalse(self.appointment.is_active)

		# restore
		res_url = reverse('restore_appointment_ajax', args=[self.appointment.id])
		resp2 = self.client.post(res_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(resp2.status_code, 200)
		data2 = resp2.json()
		self.assertTrue(data2.get('success'))
		self.appointment.refresh_from_db()
		self.assertTrue(self.appointment.is_active)

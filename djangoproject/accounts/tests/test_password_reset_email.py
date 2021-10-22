from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail

class PasswordResetEmail(TestCase):

    def setUp(self):
        User.objects.create(username='johntron',email='john@jackie.com',password='1234abcda')
        url=reverse('password_reset')
        self.response=self.client.post(url,{'email':'john@jackie.com'})
        self.email=mail.outbox[0]

    def test_email_subject(self):
        self.assertEquals('[Django Boards] Please reset your password',self.email.subject)


    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('johntron', self.email.body)
        self.assertIn('john@jackie.com', self.email.body)

    def test_email_to(self):
        self.assertEqual(['john@jackie.com',], self.email.to)

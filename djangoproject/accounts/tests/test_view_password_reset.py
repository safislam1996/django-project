from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.test import TestCase
from django.urls import reverse,resolve
from django.contrib.auth.models import User
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import views as auth_views

class PasswordResetViewTest(TestCase):

    def setUp(self):
        url=reverse('password_reset')
        self.response=self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_view_func(self):
        view=resolve('/reset/')
        self.assertEquals(view.func.view_class,auth_views.PasswordResetView)

    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')

    def test_contain_form(self):
        form=self.response.context.get('form')
        self.assertIsInstance(form,PasswordResetForm)

        '''
        The view must contain two inputs: csrf and email
        '''
    def test_form_inputs(self):
        self.assertContains(self.response,'<input',2)
        self.assertContains(self.response,'type="email"',1)

class SuccesfulResetPasswordTests(TestCase):

    def setUp(self):
        email='john@don.com'
        User.objects.create(username='john',email=email,password='1234abcd')
        url=reverse('password_reset')
        self.response=self.client.post(url,{'email':email})

    def test_redirection(self):
        url=reverse('password_reset_done')
        self.assertRedirects(self.response,url)

    def test_email_sent(self):
        self.assertEquals(1,len(mail.outbox))

class InvaildResetPasswordTests(TestCase):

    def setUp(self):
        url=reverse('password_reset')
        self.response=self.client.post(url,{'email':'emaildoesntexist@email.com'})

    def test_redirect(self):
        url=reverse('password_reset_done')
        self.assertRedirects(self.response,url)

    def test_email_sent(self):
        self.assertEquals(0,len(mail.outbox))

class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/reset_done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)


#Password reset Confirm page test

class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='john', email='john@doe.com', password='123abcdef')

        '''
        create a valid password reset token
        based on how django creates the token internally:
        https://github.com/django/django/blob/1.11.5/django/contrib/auth/forms.py#L280
        '''
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)

        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/reset/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf and two password fields
        '''
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='john', email='john@doe.com', password='123abcdef')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        '''
        invalidate the token by changing the password
        '''
        user.set_password('abcdef123')
        user.save()

        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))

class PasswordResetCompleteViewTest(TestCase):
    def setUp(self):
        url=reverse('password_reset_complete')
        self.response=self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_view_function(self):
        view=resolve('/reset/complete/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)

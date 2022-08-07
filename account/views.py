
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.views import LoginView as DefaultLoginView
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse

from django.conf import settings
from django.template.loader import get_template

from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from skilldun.models import MetaData, CompanySocialMedia


# from urllib.parse import unquote

# from skilldunmain.mixins import send_mail_ses, get_unique_path
import json

import datetime

from skilldunmain.mixins import RequestAttachMixin, NextUrlMixin

from .models import (
		User,
		TempUserBeforeActive,
		ResetPasswordIndex
	)

from django.http import JsonResponse

base_url = getattr(settings, 'BASE_URL', 'https://skilldunya.com')
from_email = settings.DEFAULT_FROM_EMAIL


def testconfirmemailtemplate(request):

	context_invite = {
		'name': "John",
		"support_email": from_email,
		"help_url": base_url,
		"logo": base_url + "/static/assets/dist/img/logo.png",
		"base_url": base_url,
		"action_url": base_url,
		"login_url": base_url + "/accounts/login/",
		"username": "test@gmail.com",
	}

	return render(request, 'mail/welcome_agent.html', context=context_invite)


def signup_page_func(request):
	if request.user.is_authenticated:
		return redirect('homepage')

	data = {
		'MetaData': MetaData.objects.filter(
				active=True
			).first(),
		'CompanySocialMedia': CompanySocialMedia.objects.filter(
				active=True
			).order_by('-priority')
	}

	return render(request, 'signup.html', data)


def login_page_func(request):
	if request.user.is_authenticated:
		return redirect('homepage')

	data = {
		'MetaData': MetaData.objects.filter(
				active=True
			).first(),
		'CompanySocialMedia': CompanySocialMedia.objects.filter(
				active=True
			).order_by('-priority')
	}

	return render(request, 'login.html', data)


def reset_password(request):

	if request.method == 'POST':

		try:
			data = dict(request.POST)

			data = {k: v[0] for k, v in data.items()}

			if data['csrfmiddlewaretoken']:
				email = data['email']
				usr_obj = User.objects.filter(email=email).first()

				if usr_obj:
					if usr_obj.status:
						resetInd = ResetPasswordIndex.objects.create(email=email)

						data.pop('csrfmiddlewaretoken')

						context_reset_confirm = {
									"logo": base_url + "/static/assets/dist/img/logo.png",
									"base_url": base_url,
									"name": "{} {}".format(usr_obj.first_name, usr_obj.last_name),
									"action_url": '{}{}'.format(base_url, resetInd.get_absolute_url()),
									"operating_system": request.META.get('XDG_SESSION_TYPE'),
									"browser_name": request.META.get('HTTP_USER_AGENT'),
									"support_url": base_url
								}

						subject = "Reset password"

						sender = "Skill Dunya"

						html_ = get_template('mail/confirm_reset.html').render(context_reset_confirm)

						send_mail_ses(
									sender=from_email,
									sender_name=sender,
									recipient=data['email'],
									subject=subject,
									body_html=html_
								)

						if request.is_ajax():
							data_record = data

							return JsonResponse(data_record)
					else:
						raise Exception('User is not active, contact support')
				else:
					raise Exception('User not found with this email')
			else:
				raise Exception('CSRF Token Missing')

		except Exception as e:
			if request.is_ajax():
				err = {
					'error': str(e)
				}

				response = JsonResponse(err)
				response.status_code = 403

				return response

	else:
		return render(request, 'auth/reset_password.html', {})


def confirm_reset_password(request, slug):
	template_name = 'auth/reset_password_form.html'
	resetInd = get_object_or_404(ResetPasswordIndex, reset_id=slug)

	expire_date = resetInd.created_at + datetime.timedelta(hours=resetInd.expire_hours)
	date_now = datetime.datetime.now(tz=resetInd.created_at.tzinfo)

	if (expire_date >= date_now) and (not resetInd.used):
		if request.method == 'POST':
			data = {k: v[0] for k, v in dict(request.POST).items()}
			password = data['password']

			user = User.objects.filter(email=resetInd.email).first()

			if password == data['password2']:
				user.set_password(password)
				user.save()

				resetInd.used = True
				resetInd.save()

				messages.success(request, 'Your password was successfully updated!')
				return redirect('login')
			else:
				messages.error(request, 'Password not matched.')
	else:
		messages.error(request, 'This token is expired or used, Request again to change your password.')

		return redirect('reset_pass')

	return render(request, template_name, {})


def user_create_func(request):

	try:
		data = dict(request.POST)

		data = {k: v[0] for k, v in data.items()}

		if not data['password1'] == data['password2']:
			raise Exception('Password not matched')
		else:
			data.pop('password2')

		data['password'] = data.pop('password1')

		if data['csrfmiddlewaretoken']:
			prev_user = User.objects.filter(email=data['email']).first()
			if prev_user:
				raise Exception('User with this email is already exists.')

			email = data['email']

			temp_object = TempUserBeforeActive.objects.create(
				email=data['email'], 
				hash_object=json.dumps(data)
				)

			context = {
				'base_path': base_url,
				"username": data['email'].split('@')[0],
				"our_email": from_email,
				"email": data['email'],
				"confirm_page": '{}{}'.format(base_url, temp_object.get_absolute_url()),
				"logo": base_url + "/static/skilldun/images/logo.png",
			}
			subject = "Skill Dunya - Confirm email address"
			html_ = get_template('mail/confirm.html').render(context)

			res = send_mail(
					from_email=from_email, 
					recipient_list=[email], 
					subject=subject, 
					html_message=html_, 
					message=html_
				)

			if request.is_ajax():
				data.pop('password')
				data['status'] = 'success'

				return JsonResponse(data)
		else:
			raise Exception('CSRF Token Missing')

	except Exception as e:
		if request.is_ajax():
			err = {
				'error': str(e)
			}

			response = JsonResponse(err)
			response.status_code = 403

			return response

	return redirect('homepage')


def login_func(request):
   
	try:
		data = dict(request.POST)

		data = {k: v[0] for k, v in data.items()}

		if data['csrfmiddlewaretoken']:
			user = authenticate(username=data['email'], password=data['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
				else:
					raise Exception("User not active")
			else:
				raise Exception("Authentication failure")

			if request.is_ajax():
				data.pop('password')
				data['status'] = 'success'

				return JsonResponse(data)
		else:
			raise Exception('CSRF Token Missing')

	except Exception as e:
		if request.is_ajax():
			err = {
				'error': str(e)
			}

			response = JsonResponse(err)
			response.status_code = 403

			return response

	return redirect('homepage')


def confirm_user_create(request, slug):
	temp_user = TempUserBeforeActive.objects.get(slug=slug)

	if temp_user:
		if temp_user.is_active == 1:
			temp_hash_res = json.loads(temp_user.hash_result())

			temp_hash_res.pop('csrfmiddlewaretoken')

			user = User.objects.create_user(**temp_hash_res)

	return redirect('homepage')


def user_update_func(request):
	try:
		data = dict(request.POST)
		data = {k:v[0] for k,v in data.items()}

		if 'password' not in data and data['csrfmiddlewaretoken']:
			data.pop('csrfmiddlewaretoken')

			user = User.objects.filter(userid=data.pop('userid'), email=data['email'])
			user.update(**data)

		if request.is_ajax():

			user = user.first()
			data_record = user.__dict__
			data_record.pop('_state')
			data_record.pop('userid')
			data_record.pop('password')
			data_record.pop('profile_picture')
			data_record['title_position'] = user.title_position()
			data_record['role_text'] = user.role_text

			return JsonResponse(data_record)

	except Exception as e:
		if request.is_ajax():
			err = {
				'error': str(e)
			}

			response = JsonResponse(err)
			response.status_code = 403

			return response

	return redirect('myCompany')

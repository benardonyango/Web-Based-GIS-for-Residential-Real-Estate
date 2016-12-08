from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from section.models import *
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout


	)


class SearchSellForm(forms.Form):
	search_sale_rent = forms.ChoiceField(
		choices=([("",'Sale or Rent'),("Sale","Sale"),("Rent","Rent")]),
		required=False,label='')
	

	search_housetype = forms.ChoiceField(
		choices=([("",'Choose House Type'),("HOUSE",'House'),("APARTMENT_FLAT",'Apartment/Flat'),
				("TOWNHOUSE",'Town House'),("DUPLEX",'Duplex')]),
				required=False,label='')
		

	search_beds = forms.ChoiceField(
		choices=([("",'Choose Number of Beds'),
				(1, '1'),
				(2, '2'),
				(3, '3'),
				(4, '4'),
				(5, '5'),
				(6, '6'),
				(7, '7')]),
				required=False,label='')

		


	search_baths = forms.ChoiceField(
		choices=([("",'Choose Number of Baths'),
				(1, '1'),
				(2, '2'),
				(3, '3'),
				(4, '4'),
				(5, '5'),
				(6, '6'),
				(7, '7')]),
				required=False,label='')

		

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		
		if username and password:

			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exist")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect password")

			if not user.is_active:
				raise forms.ValidationError("This user is no longer active")

		return super(UserLoginForm, self).clean(*args,**kwargs)








class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email Address')
	email2 = forms.EmailField(label='Confirm Email')
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password'


		]


	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Emails must match")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")
		return email
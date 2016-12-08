from searchlist_views.views import SearchListView
from searchlist_views.filters import BaseFilter
from .forms import SearchSellForm
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import redirect
from django.shortcuts import render , get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers
from .models import Sell

from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout


	)

from .forms import UserLoginForm, UserRegisterForm




def index(request):
	intro = loader.get_template("index.html")
	return HttpResponse(intro.render())

def map(request):
	return render(request, 'map2.html')


class SellFilter(BaseFilter):
	search_fields = {
		"search_sale_rent" : ["sale_rent"],
		"search_housetype" : ["house_type"],
		"search_beds" : ["beds"],
		"search_baths" : ["baths"],
	}


class properties(SearchListView):
	model = Sell
	template_name = "buy_rent.html"
	form_class = SearchSellForm
	filter_class = SellFilter
	




@api_view(['GET'])
def get_properties(request):
	result = Sell.objects.all()
	data = serializers.serialize('json', result)
	return Response(data, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['GET'])
def properties_filter(request):
	request_data = request.query_params
	filtered_fields = request_data['fields']

	kwargs = {}

	if "sale_rent" in filtered_fields:
		kwargs['sale_rent'] = request_data['sale_rent']
	if "price" in filtered_fields:
		price = request_data['price'] # e.g (150, 400) 
		price_values = price[1:][:-1].split(',')
		min_price = price_values[0]
		max_price = price_values[1]
		kwargs['price__range'] =  (min_price, max_price)
		print kwargs['price__range']
	if "house_type" in filtered_fields:
		kwargs['house_type'] = request_data['house_type']
	if "beds" in filtered_fields:
		kwargs['beds'] = request_data['beds']
	if "baths" in filtered_fields:
		kwargs['baths'] = request_data['baths']

	try:
		result = Sell.objects.filter(**kwargs)
		data = serializers.serialize('json', result)
		return Response(data, status=status.HTTP_200_OK, content_type='application/json')
		
	except:
		return Response(status=status.HTTP_400_BAD_REQUEST)



def login_view(request):
	print(request.user.is_authenticated())
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username,password=password)
		login(request,user)
		return redirect("/")

	return render(request, "form.html", {"form":form, "title":title})


def register_view(request):
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username,password=password)
		login(request, new_user)
		return redirect("/")

	context = {
		"form":form,
		"title":title


	}
	return render(request, "form.html", context)


def logout_view(request):
	logout(request)
	return redirect("/")


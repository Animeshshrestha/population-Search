import json, pdb

from django.db.models import Sum, Avg, Count, F, Q, When
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.db import IntegrityError
from django.conf import settings

from pusher import Pusher

from .models import Country, CityOrState, PopulationSearch
from .forms import CountryForm, CityOrStateForm, PopulationSearchForm


pusher = Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUHSER_CLUSTER,
    ssl=True)

def hello(request):
	"""
	This function is just for login only. It does not work.

	"""

	return render(request,'login.html')

def logout_view(request):
	"""
		Logout view that log outs the session of logged in user
	"""

	logout(request)
	return redirect('population-details')

def population_max():
	"""
		This function returns the top 3 max population from the available country
	"""
	total = list(PopulationSearch.objects.values(
				'country__name').\
				order_by('-total').\
				annotate(
					total=Sum(F('no_of_male')+F('no_of_female'))
				)[:3]
			)
	return total


def max_three_population(request):
	"""
		Function that calls the population_max() function and returns
		the data when the home page is loaded at first to display the
		max three population
	"""
	if request.method == "GET":
		total = population_max()
	
		return JsonResponse(total, safe=False)

class AdminAuthentication(View):
	"""
		View for authenticating the admin user
	"""

	template_name = 'login.html'

	def get(self,request):

		return render(request,self.template_name)
	
	def post(self,request):

		user_name = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=user_name, password=password)

		if user is not None:
			login(request,user)
			response = {'status':200}
			return JsonResponse(response,safe=False)
		else:
			response = {'status':500}
			return JsonResponse(response, safe=False)

class CountryListView(View):
	"""
	View that returns the list of countries
	"""

	template_name = 'country.html'

	def get(self,request):

		list_of_countrys = Country.objects.all().values('name','id')
		context_dict = {
			'countrys':list_of_countrys
		}

		if 'list' in request.GET:
			data = []
			for country in list_of_countrys:
				data.append({
					'name':country.get('name'),
					'id':country.get('id')
				})
			return JsonResponse(data,safe=False)
		else:	
			return render(request,self.template_name,context_dict)


class CountryEditView(View):
	"""
		View that allows us to perform the CRUD operation
		on Country.
	"""

	form_class = CountryForm
	
	def get(self,request):

		if 'id' in request.GET:
			print(request.GET)
			country_id = request.GET['id']
			country = Country.objects.get(id=country_id).name
			context_dict = {
				'name':country
			}
			return JsonResponse(context_dict,safe=False)

	def post(self,request):

		if request.POST.get('method') == 'DELETE':
			Country.objects.get(id=request.POST['id']).delete()
			data = {"status":"True"}
			return JsonResponse(data,safe=False)

		if request.POST.get('method') == 'EDIT':
			country = Country.objects.get(id=request.POST['country_id'])

		try:
			form = self.form_class(request.POST, instance=country)
		except:
			form = self.form_class(request.POST)

		if form.is_valid():
			form.save()
			data = {"status":"True",'message':"Country Added Sucessfully"}
			return JsonResponse(data,safe=False)

		else:
			data = {"status":"False","errors":form.errors.as_json()}
			return JsonResponse(data,safe=False)

class CityListView(View):
	"""
	View that returns the list of city according to the countries
	"""

	template_name = 'city.html'

	def get(self,request):

		city_lists = CityOrState.objects.all()

		if 'list' in request.GET:
			
			try:
				country = Country.objects.get(id=request.GET['id'])
			except:
				country = Country.objects.get(name=request.GET['country'])

			city_state  = CityOrState.objects.filter(country = country)
			data = []
			for city in city_state:
				data.append({
					'name': city.city_or_state,
					'id':city.id
				})
			return 	JsonResponse(data,safe=False)
		
		context_dict = {
			'city_list':city_lists
		}
		
		return render(request,self.template_name,context_dict)

class CityEditView(View):
	"""
		View that allows us to perform the CRUD operation
		on City/State.
	"""

	form_class = CityOrStateForm

	def get(self,request):

		if 'id' in request.GET:
			city_id = request.GET['id']
			city_or_state = CityOrState.objects.get(id=city_id)
			context_dict = {
				'country_id':city_or_state.country_id,
				'city_or_state':city_or_state.city_or_state
			}
			return JsonResponse(context_dict,safe=False)

	def post(self,request):

		if request.POST.get('method') == 'DELETE':

			CityOrState.objects.get(id=request.POST['id']).delete()
			data = {"status":"True"}
			return JsonResponse(data,safe=False)
		
		country = Country.objects.get(id=request.POST['country'])
		try:
			city = CityOrState.objects.get(id=request.POST['city-id'])
			form = self.form_class(request.POST, instance=city)
			
		except:
			form = self.form_class(request.POST)

		if form.is_valid():
			try:
				data = form.save(commit=False)
				data.country = country
				data.save()
				data = {"status":"True",'message':"City Added Sucessfully"}
				return JsonResponse(data,safe=False)
			except Exception as e:
				data = {"status":"False","errors":e.message_dict}
				return JsonResponse(data,safe=False)

		else:
			data = {"status":"False","error":form.errors.as_json()}
			return JsonResponse(data,safe=False)

class PopulationList(View):
	"""
	View that returns the list of population according to the countries
	and cities
	"""

	template_name = 'population.html'

	def get(self,request):

		if 'id' in request.GET:
			country_id = request.GET['id']
			population_detail = PopulationSearch.objects.filter(country__id=country_id)
			data = []
			for population in population_detail:
				data.append({
					'id':population.id,
					'state':population.city_or_state.city_or_state,
					'male':population.no_of_male,
					'female':population.no_of_female,
					'age_group':population.get_group_display()
				})
			return JsonResponse(data,safe=False)
		
		return render(request,self.template_name)

class PopulationEdit(View):
	"""
		View that allows us to perform the CRUD operation
		on Population.
	"""

	form_class = PopulationSearchForm

	def get(self,request):

		if 'id' in request.GET:
			population_id = request.GET['id']
			population = PopulationSearch.objects.get(id=population_id)
			context_dict = {
				'country_id':population.country.id,
				'city_or_state':population.city_or_state.id,
				'group':population.group,
				'no_of_male':population.no_of_male,
				'no_of_female':population.no_of_female
			}
			return JsonResponse(context_dict,safe=False)


	def post(self,request):

		if request.POST.get('method') == 'DELETE':
			PopulationSearch.objects.get(id=request.POST['id']).delete()
			data = {"status":"True"}
			return JsonResponse(data,safe=False)

		country = Country.objects.get(id=request.POST['country'])
		city = CityOrState.objects.get(id=request.POST['city_or_state'])

		try:
			population = PopulationSearch.objects.get(id=request.POST['id'])
			form = self.form_class(request.POST,instance=population)

		except:
			form = self.form_class(request.POST)

		if form.is_valid():
			try:
				data = form.save(commit=False)
				data.country = country
				data.city_or_state=city
				data.save()
				
				pusher.trigger('my-channel', 'my-event', {'message': population_max()})
				data = {"status":"True",'message':"Population Added Sucessfully"}
				return JsonResponse(data,safe=False)
			except Exception as e:

				data = {"status":"False","errors":e.message_dict}
				return JsonResponse(data,safe=False)
		else:
	
			data = {"status":"False","error":form.errors.as_json()}
			return JsonResponse(data,safe=False)


def all_countries_population(request):
	"""
	Function that returns the total population
	by group according to the selected Country,
	State and Gender
	"""

	if request.method == "GET":

		country = request.GET.get('country','All')
		state = request.GET.get('state','All')
		gender = request.GET.get('gender','All')
		
		filters = {}
		sum = F('no_of_male')+F('no_of_female')
		if country !='All':
			filters['country__name']=country
		if state !='All':
			filters['city_or_state__city_or_state']=state
		if gender == 'male':
			sum = F('no_of_male')
		if gender == 'female':
			sum = F('no_of_female')

		old = PopulationSearch.objects.filter(**filters,group='ol').aggregate(old=Sum(sum))
		young = PopulationSearch.objects.filter(**filters,group='yo').aggregate(young=Sum(sum))
		child = PopulationSearch.objects.filter(**filters,group='ch').aggregate(child=Sum(sum))
		data = [old,young,child]
		return JsonResponse(data, safe=False)

class PopulationDetails(View):
	"""
	View that returns the list of countries on the 
	home page 
	"""

	template_name = 'populationdetails.html'

	def get(self,request):

		list_of_countrys = Country.objects.all().values('name','id')
		
		context_dict = {
			'countrys':list_of_countrys
		}
		return render(request, self.template_name, context_dict)


		




		


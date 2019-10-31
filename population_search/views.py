import json
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.db import IntegrityError

from .models import Country, CityOrState, PopulationSearch
from .forms import CountryForm, CityOrStateForm, PopulationSearchForm

# from pusher import Pusher

# pusher = Pusher(
#     app_id='814492',
#     key='103ebaaa5395c0e58d67',
#     secret='4eb627ea6d3ec2136429',
#     cluster='ap2',
#     ssl=True)

def hello(request):
	# pusher.trigger(u'a_channel', u'an_event', {u'message': 'hello world'})

	return render(request,'sample.html')

class CountryListView(View):

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

	template_name = 'city.html'

	def get(self,request):

		city_lists = CityOrState.objects.all()

		if 'list' in request.GET:
			country = Country.objects.get(id=request.GET['id'])
			city_state  = CityOrState.objects.filter(country = country)
			data = []
			for city in city_state:
				data.append({
					'name': city.city_or_state
				})
			print("for country",data)
			return 	JsonResponse(data,safe=False)
		
		context_dict = {
			'city_list':city_lists
		}
		
		return render(request,self.template_name,context_dict)

class CityEditView(View):

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
		print(request.POST)
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
				print(e)
				data = {"status":"False","errors":e.message_dict}
				return JsonResponse(data,safe=False)

		else:
			
			data = {"status":"False","error":form.errors.as_json()}
			return JsonResponse(data,safe=False)

class PopulationList(View):

	template_name = 'population.html'

	def get(self,request):

		if 'id' in request.GET:
			country_id = request.GET['id']
			population_detail = PopulationSearch.objects.filter(country__id=country_id)
			data = []
			for population in population_detail:
				data.append({
					'id':population.id,
					'state':population.city_or_state,
					'male':population.no_of_male,
					'female':population.no_of_female,
					'age_group':population.get_group_display()
				})
			print(data)
			return JsonResponse(data,safe=False)

		return render(request,self.template_name)

class PopulationEdit(View):

	form_class = PopulationSearchForm

	def get(self,request):

		if 'id' in request.GET:
			population_id = request.GET['id']
			population = PopulationSearch.objects.get(id=population_id)
			context_dict = {
				'country_id':population.country.id,
				'city_or_state':population.city_or_state,
				'group':population.group,
				'no_of_male':population.no_of_male,
				'no_of_female':population.no_of_female
			}
			print(context_dict)
			return JsonResponse(context_dict,safe=False)


	def post(self,request):

		if request.POST.get('method') == 'DELETE':
			PopulationSearch.objects.get(id=request.POST['id']).delete()
			data = {"status":"True"}
			return JsonResponse(data,safe=False)

		country = Country.objects.get(id=request.POST['country'])
		print(request.POST)
		try:
			population = PopulationSearch.objects.get(id=request.POST['id'])
			form = self.form_class(request.POST,instance=population)
			print(" I am editing")
		except:
			form = self.form_class(request.POST)
			print(" I am here")
		if form.is_valid():
			try:
				data = form.save(commit=False)
				data.country = country
				data.save()
				data = {"status":"True",'message':"Population Added Sucessfully"}
				return JsonResponse(data,safe=False)
			except Exception as e:
				data = {"status":"False","errors":e.message_dict}
				return JsonResponse(data,safe=False)
		else:
			print("form was not valid")
			data = {"status":"False","error":form.errors.as_json()}
			return JsonResponse(data,safe=False)


		




		


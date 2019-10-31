from django.db.models import Sum, Avg, Count, F, Q, When

from .models import Country, CityOrState, PopulationSearch

def max_three_population():

	total = PopulationSearch.objects.values(
			'country__name').\
			order_by('-total').\
			annotate(
				total=Sum(F('no_of_male')+F('no_of_female'))
			)[:3]
	return total
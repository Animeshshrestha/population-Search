from django.contrib import admin

from .models import Country, CityOrState, PopulationSearch

admin.site.register(Country)
admin.site.register(CityOrState)
admin.site.register(PopulationSearch)
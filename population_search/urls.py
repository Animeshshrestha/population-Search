from django.urls import path

from .views import *

urlpatterns = [
    path('hi/', hello, name='hello'),
    path('country/', CountryListView.as_view(),name='country'),
    path('country-edit/', CountryEditView.as_view(),name='country-edit'),
    path('city/', CityListView.as_view(),name='city'),
    path('city-edit/', CityEditView.as_view(),name='city-edit',),
    path('population-list/', PopulationList.as_view(), name='population'),
    path('population-edit/', PopulationEdit.as_view(), name='population-edit'),
    path('', PopulationDetails.as_view(), name='population-details'),
    path('max-three-population/', max_three_population, name='max-population'),
    path('all-population/', all_countries_population, name='all-population')
]
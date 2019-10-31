from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from .models  import CityOrState, Country, PopulationSearch

class CountryForm(forms.ModelForm):

    class Meta:
        model = Country
        fields = ('name',)
    
    def clean(self):

        cleaned_data = super(CountryForm,self).clean()
        country_name = cleaned_data.get('name')
        if Country.objects.filter(name__iexact=country_name).exists():
            self.add_error('name',"Country Name already exists")
        return cleaned_data

class CityOrStateForm(forms.ModelForm):

    class Meta:
        model = CityOrState
        fields = ('city_or_state',)


class PopulationSearchForm(forms.ModelForm):

    class Meta:
        model = PopulationSearch
        fields = ('group', 'city_or_state', 'no_of_male', 'no_of_female')

        

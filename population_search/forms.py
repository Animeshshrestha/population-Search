from django import forms

from .models  import CityOrState, Country

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
        fields = ('city_or_state','country',)

    def __init__(self,country, *args, **kwargs):
        super(CityOrStateForm, self).__init__(*args, **kwargs)
        self.fields['country'].queryset = Country.objects.filter(name=country)
    
    def clean(self):

        cleaned_data = super(CityOrStateForm,self).clean()
        print(cleaned_data)
        country = Country.objects.get(name=cleaned_data['country'])
        city = cleaned_data['city_or_state']
        if CityOrState.objects.filter(country=country,city_or_state__iexact=city).exists():
            self.add_error('city_or_state',"Country with that City Name already exists")
        return cleaned_data
        

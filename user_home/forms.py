from django import forms
from django.core.validators import RegexValidator
from .models import User_Address

class AddressForm(forms.ModelForm):
    name_validator = RegexValidator(r'^[a-zA-Z ]*$', 'Name must contain only letters and spaces')
    text_validator = RegexValidator(r'^[a-zA-Z0-9 ,-]*$', 'Field must contain only letters, digits, spaces, commas, and hyphens')

    class Meta:
        model = User_Address
        fields = ['name', 'phone_number', 'house_name', 'landmark', 'city', 'pincode', 'district', 'state', 'country']
    
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['house_name'].widget.attrs['placeholder'] = 'Enter House name'
        self.fields['landmark'].widget.attrs['placeholder'] = 'Enter landmark'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter city'
        self.fields['pincode'].widget.attrs['placeholder'] = 'Enter pin code'
        self.fields['district'].widget.attrs['placeholder'] = 'Enter district'
        self.fields['state'].widget.attrs['placeholder'] = 'Enter state'
        self.fields['country'].widget.attrs['placeholder'] = 'Enter country'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-lg'
    
    def clean_name(self):
        name = self.cleaned_data['name']
        self.name_validator(name)
        return name
    
    def clean_house_name(self):
        house_name = self.cleaned_data['house_name']
        self.text_validator(house_name)
        return house_name
    
    def clean_landmark(self):
        landmark = self.cleaned_data['landmark']
        self.text_validator(landmark)
        return landmark
    
    def clean_city(self):
        city = self.cleaned_data['city']
        self.text_validator(city)
        return city
    
    def clean_district(self):
        district = self.cleaned_data['district']
        self.text_validator(district)
        return district
    
    def clean_state(self):
        state = self.cleaned_data['state']
        self.text_validator(state)
        return state
    
    def clean_country(self):
        country = self.cleaned_data['country']
        self.text_validator(country)
        return country
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError('Phone number must contain only digits')
        return phone_number
        
    def clean_pincode(self):
        pincode = self.cleaned_data['pincode']
        if not pincode.isdigit() or len(pincode) != 6:
            raise forms.ValidationError('Invalid pin code')
        return pincode

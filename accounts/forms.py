from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from . models import Account

class RegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=100, validators=[RegexValidator(r'^[a-zA-Z ]+$', message="Enter a valid name.")])
    phone_number = forms.CharField(max_length=10, validators=[RegexValidator(r'^[0-9]+$', message="Enter a valid phone number.")])
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm Password',
    }))

    class Meta:
        model = Account
        fields = ['name', 'phone_number', 'email', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs )
        self.fields['name'].widget.attrs['placeholder'] = 'Enter your name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'input100'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

        # validate password
        try:
            validate_password(password)
        except forms.ValidationError as e:
            self.add_error('password', e)

        return cleaned_data

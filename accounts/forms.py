from django import forms
from .models import Account, user_profile


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'enter password',
        'class' : 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'confirm password',
        'class' : 'form-control',
    }))


    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number','password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'FIRST NAME'
        self.fields['last_name'].widget.attrs['placeholder'] = 'LAST NAME'
        self.fields['email'].widget.attrs['placeholder'] = 'E-MAIL'
        self.fields['password'].widget.attrs['placeholder'] = 'ENTER PASSWORD'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'CONFIRM PASSWORD'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'PHONE NUMBER'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('password does not matched!')
        


class userForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')
    
    def __init__(self, *args, **kwargs):
        super(userForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid' : ('images files only')}, widget=forms.FileInput)
    class Meta:
        model  = user_profile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
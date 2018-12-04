from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Server,Client

class DateInput(forms.DateInput):
    input_type = 'date'
class ClientSignUpForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ('name', 'phone', 'gender','birth_date', 'address', 'image', 'password1', 'password2')
        widgets = {
            'birth_date': DateInput()
        }

class ServerSignUpForm(UserCreationForm):
    class Meta:
        model = Server
        fields = ('name', 'phone', 'gender', 'birth_date','address','category','image', 'password1', 'password2')
        widgets = {
            'birth_date': DateInput()
        }

class AddExpForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['experience']

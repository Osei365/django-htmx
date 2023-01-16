from django import forms
from .models import DataFile, Charts, Dashboard, User  
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField


class DataForm(forms.ModelForm):

    class Meta:
        model = DataFile
        fields = ['workingfile'] 
        widgets = {
            'workingfile': forms.FileInput(attrs={'class': 'form-control'})
        }

class ChartForm(forms.ModelForm):

    class Meta:
        model = Charts
        fields = ['data', 'X', 'Y']
        widgets= {
            'data': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'X' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'Y' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

class PivotForm(forms.Form):

    agg_choices = [
        ('Min', 'Min'),
        ('Max', 'Max'),
        ('Avg', 'Avg'),
        ('Count', 'Count')
    ]
    groupby = forms.ChoiceField(choices='', widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    focus = forms.ChoiceField(choices='', widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    agg = forms.ChoiceField(choices= agg_choices, widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    table_title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

class UpdateForm(forms.ModelForm):

    class Meta:
        model = Dashboard
        fields =['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm'})
        }

class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields= ['username', 'password1', 'password2']
        # widgets= {
        #     'username': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        #     'password1' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        #     'password2' : forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        # }

class LoginForm(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control', 'id':'floatingInput'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id':'floatingPassword'}))
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tempus_dominus.widgets import DateTimePicker
from django import forms
from .models import *

class OrderForm(ModelForm):
    reserve_date = forms.DateTimeField(widget=DateTimePicker(
    options={
        'useCurrent': True,
        'collapse': True,
        },
    attrs={
        'append': 'fa fa-calendar',
        'icon_toggle': True,
        }))
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs.update({'class' : 'form-control'})
        self.fields['product'].widget.attrs.update({'class' : 'form-control'})
        self.fields['status'].widget.attrs.update({'class' : 'form-control'})
        self.fields['note'].widget.attrs.update({'class' : 'form-control'})

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'style' : 'border-radius: 20px; width: 275px; height: 40px;', 'placeholder' : '  Username'})
        self.fields['email'].widget.attrs.update({'style' : 'border-radius: 20px; width: 275px; height: 40px;', 'placeholder' : '  Email'})
        self.fields['password1'].widget.attrs.update({'style' : 'border-radius: 20px; width: 275px; height: 40px;', 'placeholder' : '  Password'})
        self.fields['password2'].widget.attrs.update({'style' : 'border-radius: 20px; width: 275px; height: 40px;', 'placeholder' : '  Re-enter Password'})

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'membership']

class ReservationForm(ModelForm):
    reserve_date = forms.DateTimeField(widget=DateTimePicker(
    options={
        'useCurrent': True,
        'collapse': True,
        'minDate': '2020-07-13 00:00:00',
        'maxDate': '2024-01-20 23:59:00',

        # Calendar and time widget formatting
        'time': 'fa fa-clock-o',
        'date': 'fa fa-calendar',
        'up': 'fa fa-arrow-up',
        'down': 'fa fa-arrow-down',
        'previous': 'fa fa-chevron-left',
        'next': 'fa fa-chevron-right',
        'today': 'fa fa-calendar-check-o',
        'clear': 'fa fa-delete',
        'close': 'fa fa-times'
        },
    attrs={
        'append': 'fa fa-calendar',
        'icon_toggle': True,
        }))
    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = self.fields['product'].queryset.filter(tags__name="Reservation")
    class Meta:
        model = Order
        fields = '__all__'

        widgets = {'customer' : forms.HiddenInput(),
                   'status' : forms.HiddenInput()}

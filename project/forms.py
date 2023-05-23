from django import forms
from django.forms import ModelForm
from .models import Trip

class RegisterCustomerForm(forms.Form):
    name = forms.CharField(label='Name')
    surname = forms.CharField(label='Surname')
    age = forms.IntegerField(label='Age')
    email = forms.EmailField(label='Email')

    def __init__(self, *args, **kwargs):
        super(RegisterCustomerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RegisterTripForm(ModelForm):
    class Meta:
        model = Trip
        fields = ('tripname','description', 'date_1', 'date_2', 'price','image')


    def __init__(self, *args, **kwargs):
        super(RegisterTripForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CustomerFilterForm(forms.Form):
    customername = forms.CharField(label='Name', required = False)
    surname = forms.CharField(label='Surname', required = False)
    age = forms.IntegerField(label='Age', required = False)

    def __init__(self, *args, **kwargs):
        super(CustomerFilterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class TripFilterForm(forms.Form):
    tripname = forms.CharField(label='Name', required = False)
    date = forms.DateField(label='Date', required = False)
    price = forms.DecimalField(label='Price', required=False)

    def __init__(self, *args, **kwargs):
        super(TripFilterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


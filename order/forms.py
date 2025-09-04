from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name',
                  'phone',
                  'email', 'adress_line_one', 
                  'adress_line_two', 'country', 
                  'state', 'city', 'order_note'
                  ]
        
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Enter phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['adress_line_one'].widget.attrs['placeholder'] = 'Enter Address Line 1'
        self.fields['adress_line_two'].widget.attrs['placeholder'] = 'Enter Address Line 2'
        self.fields['country'].widget.attrs['placeholder'] = 'Enter country'
        self.fields['state'].widget.attrs['placeholder'] = 'Enter State'
        self.fields['city'].widget.attrs['placeholder'] = 'Enter city'
        self.fields['order_note'].widget.attrs['placeholder'] = 'Enter order note'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
        
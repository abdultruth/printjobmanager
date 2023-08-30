from django import forms


from .models import Order, JobType

class OrderForm(forms.ModelForm):
    job_type = forms.ModelChoiceField(queryset=JobType.objects.all())
    class Meta:
        model = Order
        fields = ['length',
                  'width',
                  'quantity',
                  'job_type',
                  'customer',
                ]
        
        widgets = {
            'length':forms.TextInput(attrs={'class':'form-control'}),
            'width':forms.TextInput(attrs={'class':'form-control'}),
            'quantity':forms.TextInput(attrs={'class':'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['length'].widget.attrs['placeholder'] = 'length e.g 1 or 0.2 ...'
        self.fields['width'].widget.attrs['placeholder'] = 'width'
        self.fields['quantity'].widget.attrs['placeholder'] = 'e.g 1 or 2 ...'
        self.fields['job_type'].widget.attrs['placeholder'] = 'select below'
        self.fields['customer'].widget.attrs['placeholder']= 'customer'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
            
    def clean(self):
        cleaned_data = super().clean()
        length = cleaned_data.get('length')
        width = cleaned_data.get('width')
        quantity = cleaned_data.get('quantity')
        job_type = cleaned_data.get('job_type')
        
        
        if length and width and quantity and job_type:
            rate = job_type.rate
            if rate is not None:
               total_price = float(rate) * float(length) * float(width) * float(quantity)
               self.instance.price = total_price
              
            

        
        
        
        

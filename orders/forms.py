from django import forms
from .models import Order
from delivery.models import Location

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pickup_location'] = forms.ModelChoiceField(
            queryset=Location.objects.filter(is_active=True),
            required=False,
            empty_label='Выберите адрес заведения',
            label='Адрес заведения (для самовывоза)'
        )

    def clean(self):
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get('delivery_method')
        pickup_location = cleaned_data.get('pickup_location')
        if delivery_method == 'pickup':
            if not pickup_location:
                self.add_error('pickup_location', 'Выберите адрес заведения для самовывоза')
            else:
                cleaned_data['delivery_address'] = pickup_location.address
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        delivery_method = self.cleaned_data.get('delivery_method')
        pickup_location = self.cleaned_data.get('pickup_location')
        if delivery_method == 'pickup' and pickup_location:
            instance.delivery_address = pickup_location.address
        if commit:
            instance.save()
        return instance
    class Meta:
        model = Order
        fields = ['delivery_method', 'payment_method', 'delivery_address', 'phone_number', 'comments']
        widgets = {
            'delivery_method': forms.Select(),
            'payment_method': forms.Select(),
            'delivery_address': forms.Textarea(attrs={'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'rows': 2}),
        }
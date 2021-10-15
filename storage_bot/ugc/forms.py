from django import forms
from django.forms import widgets
from .models import Applications, Category, Company, Product, Profile, Storage

# Тут редактируется отображение  объектов в админке Джанго

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'external_id',
            'role',
            'company',
            'change_amount',
            'change_prod'
        )
        widgets = {
            'role': forms.TextInput,
            'company': forms.TextInput,
            'change_prod': forms.TextInput,
        }

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = (
            'name',
            'region',
            'city',
            'adress',
            'phone'
        )
        widgets = {
            'name': forms.TextInput,
            'region': forms.TextInput,
            'adress': forms.TextInput,
            'city': forms.TextInput,
        }

class StorageForm(forms.ModelForm):

    class Meta:
        model = Storage
        fields = (
            'company',
            'name',
            'adress',
            'longitude',
            'latitude',
        )
        widgets = {
            'name': forms.TextInput,
            'adress': forms.TextInput,
        }

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = (
            'name',
        )
        widgets = {
            'name': forms.TextInput,
        }

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            'company',
            'storage',
            'category',
            'name',
            'measurement',
            'amount',
        )
        widgets = {
            'name': forms.TextInput,
            'measurement': forms.TextInput,
        }

class StatusForm(forms.ModelForm):

    class Meta:
        model = Applications
        fields = (
            'company',
            'storage',
            'product',
            'amount',
            'user_id',
            'status',

        )
        widgets ={
            'status': forms.TextInput,
            'product': forms.TextInput,
        }
    
    statuses = [('Accepted','Accepted'), ('Denied','Denied'), ('Waiting','Waiting'), ('Done!','Done!')]
    #Adds choice field in order to hcange the status
    def __init__(self, *args, **kwargs):
       super(StatusForm, self).__init__(*args, **kwargs)
       if self.instance.id:
           self.fields['status'] = forms.ChoiceField(
                choices= self.statuses)

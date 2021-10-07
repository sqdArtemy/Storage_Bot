from django import forms
from django.forms import widgets
from .models import Application, Category, Company, Product, Profile, Storage

# Тут редактируется отображение  объектов в админке Джанго

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'external_id',
            'role',
            'company'
        )
        widgets = {
            'role': forms.TextInput,
            'company': forms.TextInput,
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
            'location',
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
        model = Application
        fields = (
            'company',
            'storage',
            'product',
            'amount',
            'status',
        )
        widgets ={
            'status': forms.TextInput,
        }
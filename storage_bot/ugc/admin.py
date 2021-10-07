from django.contrib import admin

from .forms import CategoryForm, CompanyForm, ProductForm, ProfileForm, StatusForm, StorageForm
from .models import Application, Category, Product, Profile, Company, Storage

# Регистрация объектов в админке джанго
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'role', 'company')
    form = ProfileForm

@admin.register(Company)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'city', 'adress', 'phone')
    form = CompanyForm

@admin.register(Storage)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'adress', 'location')
    form = StorageForm

@admin.register(Category)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name',)
    form = CategoryForm

@admin.register(Product)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('company', 'storage', 'category', 'name', 'measurement', 'amount')
    form = ProductForm

@admin.register(Application)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('company', 'storage', 'product', 'amount', 'status')
    form = StatusForm
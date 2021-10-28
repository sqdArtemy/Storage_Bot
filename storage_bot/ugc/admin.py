from django.contrib import admin

from .forms import CategoryForm, CompanyForm, ProductForm, ProfileForm, StatusForm, StorageForm
from .models import Applications, Category, Product, Profile, Company, Storage

# Регистрация объектов в админке джанго
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'role', 'company',)
    form = ProfileForm

@admin.register(Company)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'city', 'adress', 'phone')
    form = CompanyForm

@admin.register(Storage)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('company', 'name', 'adress', 'latitude', 'longitude')
    form = StorageForm

@admin.register(Category)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name',)
    form = CategoryForm

@admin.register(Product)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('company', 'storage', 'category', 'name', 'measurement', 'amount')
    form = ProductForm

@admin.register(Applications)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','company', 'storage', 'product', 'amount', 'status')
    form = StatusForm

    def save_model(self, request, obj, form, change):
        super(ProfileAdmin, self).save_model(request, obj, form, change)
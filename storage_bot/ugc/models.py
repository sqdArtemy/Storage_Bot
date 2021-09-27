from django.db import models
from django.db.models.deletion import PROTECT

# Create your models here.
# Модель для профиля пользователя 
class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name = 'ID пользователя',
        unique = True
    )
    role = models.TextField(
        verbose_name = 'Роль пользователя'
    )
    company = models.TextField(
        verbose_name = 'Компания'
    )
    def __str__(self):
        return f'Id:{self.external_id}; Роль:{self.role}; Компания:{self.company}'# для более красивого отображения 

    class Meta: 
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

# Модель для профиля компании 
class Company(models.Model):
    name = models.TextField(
        verbose_name = 'Название'
    )
    region = models.TextField(
        verbose_name = 'Область'
    )
    city = models.TextField(
        verbose_name = 'Город'
    )
    adress = models.TextField(
        verbose_name = 'Адресс'
    )
    phone = models.BigIntegerField(
        verbose_name = 'Телефон'
    )
    
    def __str__(self):
        return f'{self.name}'# для более красивого отображения 

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

# Модель для склада
class Storage(models.Model):
    company = models.ForeignKey(
        to='ugc.Company',
        verbose_name='Компания',
        on_delete = models.PROTECT,
    )
    name = models.TextField(
        verbose_name = 'Название'
    )
    adress = models.TextField(
        verbose_name = 'Адресс'
    )
    location = models.TextField(
        verbose_name = 'Гео-локация'
    )

    def __str__(self):
        return f'Склад {self.name} компании {self.company}'# для более красивого отображения 
    
    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

# Модель для категорий
class Category(models.Model):
    name = models.TextField(
        verbose_name = 'Название'
    )

    def __str__(self):
        return f'{self.name}'# для более красивого отображения 
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

# Модель для товаров
class Product(models.Model):
    company = models.ForeignKey(
        to='ugc.Company',
        verbose_name='Компания',
        on_delete = models.PROTECT,
    )
    storage = models.ForeignKey(
        to='ugc.Storage',
        verbose_name='Склад',
        on_delete = models.PROTECT,
    )
    category = models.ForeignKey(
        to='ugc.Category',
        verbose_name='Категория',
        on_delete = models.PROTECT,
    )

    name = models.TextField(
        verbose_name = 'Название'
    )
    measurement = models.TextField(
        verbose_name = 'Ед. измер.'
    )
    amount = models.BigIntegerField(
        verbose_name = 'Количество'
    )

    def __str__(self):
        return f'Товар {self.name} компании {self.company} на складе {self.storage}'# для более красивого отображения 
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

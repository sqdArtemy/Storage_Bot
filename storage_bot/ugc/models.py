from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram import Bot
from storage_bot.settings import TOKEN

bot = Bot(token= TOKEN)

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
    change_amount = models.FloatField(
        verbose_name= 'Количество для изменения',
        default = 0
    )
    change_prod = models.TextField(
        verbose_name= 'Продукт для изменения',
        default = 0
    )
    selected_category = models.ForeignKey(
        'Category',
        on_delete=PROTECT
    )
    change_measurement = models.TextField(
        verbose_name= 'Ед. изм.',
        default = 0
    )
    selected_storage = models.TextField(
        verbose_name= 'Выбранный склад',
        default = 0
    )
    current_page = models.IntegerField(
        verbose_name= 'Действующая страница',
        default = 0,
    )
    previous_page = models.IntegerField(
        verbose_name= 'Предыдущая страница',
        default = 0,
    )
    state = models.TextField(
        verbose_name = 'State of addition'
    )
    create_name = models.TextField(
        verbose_name= 'Name of new product',
        default= 0
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
        return f'{self.name}'# in order to make django-admin profile good-looking

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
    latitude = models.FloatField(
        verbose_name = 'Широта'
    )
    longitude = models.FloatField(
        verbose_name= 'Долгота'
    )

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

# Модель для категорий
class Category(models.Model):
    name = models.TextField(
        verbose_name = 'Название'
    )

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

# Модель для товаров
class Product(models.Model):
    company = models.TextField(
        verbose_name='Компания',
    )
    storage = models.TextField(
        verbose_name='Склад',
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
    amount = models.FloatField(
        verbose_name = 'Количество'
    )

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

# Модель для заявок
class Applications(models.Model):
    company = models.TextField(
        verbose_name='Компания',
    )
    storage = models.TextField(
        verbose_name='Склад',
        default='sample'
    )
    product = models.TextField(
        verbose_name='Товар',
    )
    amount = models.FloatField(
        verbose_name='Количество',
    )
    user_id = models.PositiveIntegerField(
        verbose_name = 'ID пользователя',
    )
    status = models.TextField(
        verbose_name = 'Status',
    )
    reason = models.TextField(
        verbose_name='Reason of denying',
        default=0
    )
    class Meta:
        verbose_name = 'Заявка',
        verbose_name_plural = 'Заявки'

# this funcion detects if application status was changed
@receiver(post_save, sender = Applications)
def applications_handler(sender, instance: Applications, **kwargs):
    # cheks status of applications
    application = instance
    if str(application.status) == 'Accepted':

        # recieves actual infirmation about amount of product in the storage
        obj = Product.objects.filter(name = application.product, company = application.company, storage = application.storage).get()
        field_object = Product._meta.get_field('amount')
        amount_value = getattr(obj, field_object.attname)
                    
        # checks whether amount of product is enough to change
        
        if((0 > application.amount and abs(application.amount) <= amount_value) or (application.amount > 0)):
            Product.objects.filter(name = application.product, company = str(application.company), storage = str(application.storage)).update(amount = (amount_value + application.amount))
            Applications.objects.filter(company = str(application.company), product = application.product, storage = str(application.storage)).update(status = 'Done!')
            bot.send_message(chat_id = application.user_id, text =  f'✅Your application for changing {application.product} to {application.amount} was accepted!✅')
        else:
            Applications.objects.filter(company = application.company, product = application.product, storage = application.storage).update(status = 'Denied')

    elif str(application.status) == 'Denied':
        bot.send_message(chat_id = application.user_id, text =  f'❌Your application for changing {application.product} to {application.amount} was denied! ❌\nReason:  {application.reason}')
        Applications.objects.filter(company = str(application.company), product = application.product, storage = str(application.storage)).update(status = 'Done!')
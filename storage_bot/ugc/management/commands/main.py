from os import name, stat_result
from re import U
from storage_bot.settings import TOKEN
from telegram.ext import *
from telegram import *

from django.core.management.base import BaseCommand
from ugc.models import Profile, Company, Storage, Category, Product

# Пресеты кнопок
button_companies = 'Компании'
button_storages = 'Склады'
button_categories  = 'Категории товаров'
button_products = 'Товары'
button_info_c = 'Информация о компании'
button_info_s = 'Информация о складе'
button_back = 'Назад'

# Кнопки изменения количества
BTN_PLUS = "callback+"
BTN_MINUS = "callback-"
BTN_PROD = "callback1"
BTN_SEND = "send_request"

user_roles = ['Admin', 'Lab', 'S-Manager']

# Отображает кнопочное меню в зависимоти от выбора категории
def menu(update: Update, comp, m_type):
    if m_type == 'companies':
        update.message.reply_text(
            text = f'Меню для компании: {comp}',
            reply_markup = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text = button_storages),
                        KeyboardButton(text = button_info_c),
                    ],
                    [
                        KeyboardButton(text = button_back),
                    ],
                ],
                resize_keyboard= True
            )
        )
    elif m_type == 'storages':
        update.message.reply_text(
            text = f'Меню для склада: {comp}',
            reply_markup = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text = button_categories),
                        KeyboardButton(text = button_info_s),
                    ],
                    [
                        KeyboardButton(text = button_back),
                    ],
                ],
                resize_keyboard= True
            )
        )


# Создаёт определённые кнопки в заивисимости от выбранной категории
def selection(update: Update, b_type):
    buttons = []
    # Собирает всю информацию со всех едениц, опять же, зависит от того, какую категорию мы выбираем
    items_db = b_type.objects.all()
    
    # Проверяет принадлежит ли единица к выбранной компании
    if b_type == Storage:
        for item in items_db:
            if company_id == item.company:
                buttons.append(KeyboardButton(text = item.name))
    elif b_type == Product:
        for item in items_db:
            if company_id == item.company and storage_id == item.storage and categ_id == item.category:
                buttons.append(KeyboardButton(text = item.name))
    else:
        for item in items_db:
            buttons.append(KeyboardButton(text = item.name))
    
    update.message.reply_text(
            text = 'Список: ',
            reply_markup= ReplyKeyboardMarkup(
                keyboard=[
                    buttons,
                    [
                        KeyboardButton(text = button_back),
                    ]    
                ],
                resize_keyboard= True
            )  
        )

# Выводит информацию о предприятии
def info_about(update: Update, inf):
    if inf == Company:
        update.message.reply_text(
            text = f"Название: {company_id.name} \n Область: {company_id.region} \n Город: {company_id.city} \n Адрес: {company_id.adress} \n Телефон: +{company_id.phone}",
            reply_markup = ReplyKeyboardMarkup(
                keyboard = [
                    [
                        KeyboardButton(text = button_back),
                    ],
                ],
                resize_keyboard= True
            )
        )
    elif inf == Storage:
        update.message.reply_text(
            text = f"Название: {storage_id.name} \n Адрес: {storage_id.adress} \n Локация: {storage_id.location}",
            reply_markup = ReplyKeyboardMarkup(
                keyboard = [
                    [
                        KeyboardButton(text = button_back),
                    ],
                ],
                resize_keyboard=True
            )
        )


# Создание инлайн клавиатуры в отдельной функции, чтобы потом навесить её на любое сообщение
def base_inline_keyboard():
    products_db = Product.objects.all()
    for product in products_db:
        if product.name == prod_id.name and product.company == company_id and product.storage == storage_id:
            BTNS={
                BTN_PROD: product.amount,
                BTN_PLUS: "+",
                BTN_MINUS: "-",
                BTN_SEND: "Send",
            }
   
    keyboard = [
        [
            InlineKeyboardButton(BTNS[BTN_PROD], callback_data= BTN_PROD),
        ],
        [
            InlineKeyboardButton(BTNS[BTN_PLUS], callback_data = BTN_PLUS),
            InlineKeyboardButton(BTNS[BTN_MINUS], callback_data = BTN_MINUS),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

# Вывод меню изменения количества товара
def product_adjustments(update, prod):
    update.message.reply_text(
        text = f'{prod.name} ({prod.measurement})',
        reply_markup = base_inline_keyboard()
    )

# Обработка всех инлайн кнопок 
def keyboard_callback_handler(update: Update, context: CallbackContext):

    chat_id = update.effective_message.chat_id
    query = update.callback_query
    data = query.data

    products_db = Product.objects.all()
    for item in products_db:
        if item.name == prod_id.name and item.company == company_id and item.storage == storage_id:
            p_amount = item.amount

    # Записывает роль юзера для дальнейшей проверки
    profiles_db = Profile.objects.filter(external_id = chat_id)
    for item in profiles_db:
        user_role = item.role
        user_company = item.company
    
    if data == BTN_PLUS:
        if (user_role == user_roles[0] or user_role == user_roles[2]) and str(user_company) == str(company_id):
        # Проверяет все условия, чтобы редактировался только товар определённой компании на определёном складе
            Product.objects.filter(name = prod_id.name, company = company_id, storage = storage_id).update(amount = p_amount + 1)
            query.edit_message_text(
                text=f'{prod_id.name} ({p_amount + 1} {prod_id.measurement})',
                reply_markup=base_inline_keyboard(),
                )
        else:
            query.answer('У вас нет разрешения на это.\n(Неподходящая роль/Склад не вашей компании)', True) # Выдаёт уведомление о невозможности действия

    if data == BTN_MINUS:
        if (user_role == user_roles[0] or user_role == user_roles[1]) and str(user_company) == str(company_id):
            # Проверяет все условия, чтобы редактировался только товар определённой компании на определёном складе
            Product.objects.filter(name = prod_id.name, company = company_id, storage = storage_id).update(amount = p_amount - 1)

            query.edit_message_text(
                text=f'{prod_id.name} ({p_amount - 1} {prod_id.measurement})',
                reply_markup=base_inline_keyboard(),
                )
        else: 
            query.answer('У вас нет разрешения на это.\n(Неподходящая роль/Склад не вашей компании)', True) # Выдаёт уведомление о невозможности действия

    else:
        pass

# Проверяет все сообщения от пользователя
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id

    # Добавляет юзеров в профиль
    p, _ = Profile.objects.get_or_create(
        external_id = chat_id,
    )
    
    # Проверяет были ли введены ключевые слова
    if text == button_companies:
        return selection(update, Company)

    elif text == button_storages:
        return selection(update, Storage)

    elif text == button_info_s:
        return info_about(update = update, inf = Storage)

    elif text == button_info_c:
        return info_about(update = update, inf = Company)
    
    elif text == button_categories:
        return selection(update, Category)

 
    companies_db = Company.objects.all()
    for company in companies_db:
        if text == company.name:
            global company_id
            company_id = company

            return menu(update = update, comp = company, m_type = 'companies')

    storages_db = Storage.objects.all()
    for storage in storages_db:
        if text == storage.name:
            global storage_id
            storage_id = storage

            return menu(update = update, comp = storage, m_type = 'storages')

    categories_db = Category.objects.all()
    for category in categories_db:
        if text == category.name:
            global categ_id
            categ_id = category

            return selection(update, Product)

    products_db = Product.objects.all()
    for product in products_db:
        if text == product.name:
            global prod_id, prod_amount
            prod_id = product
            prod_amount = product.amount

            return product_adjustments(update, product)

    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text = button_companies),
            ],
        ],
        resize_keyboard = True        
    )

    update.message.reply_text(
        text = 'Здравсвтуйте, выберите компанию:',
        reply_markup = reply_markup,
    )

# Связь с джанго через команду
class Command(BaseCommand):
    help = 'Storage Bot'
    
    def handle(self, *args, **kwargs):
        updater = Updater(
            token = TOKEN,
            use_context = True,
        )

        updater.dispatcher.add_handler(MessageHandler(filters = Filters.all, callback = message_handler))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback=keyboard_callback_handler))

        updater.start_polling()
        updater.idle()

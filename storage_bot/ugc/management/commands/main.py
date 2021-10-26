from os import name
from re import U

from storage_bot.settings import TOKEN
from telegram.ext import *
from telegram import *

from django.core.management.base import BaseCommand
from ugc.models import Applications, Profile, Company, Storage, Category, Product

# Пресеты кнопок
button_companies = 'Companies'
button_storages = 'Storages'
button_categories  = 'Categories'
button_products = 'Products'
button_info_c = 'Info about Comapany'
button_info_s = 'Info about Storage'
button_back = 'Back'

# Кнопки изменения количества
BTN_PLUS = "callback+"
BTN_MINUS = "callback-"
BTN_PROD = "empty_callback"
BTN_SEND = "send_request"

user_roles = ['Admin', 'Lab', 'S-Manager']

def get_id(update: Update):
    chat_id = update.effective_message.chat_id
    return chat_id

# Отображает кнопочное меню в зависимоти от выбора категории
def menu(update: Update, comp, m_type):
    if m_type == 'companies':
        update.message.reply_text(
            text = f'Menu for company: {comp}',
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
    if m_type == 'storages':
        update.message.reply_text(
            text = f'Menu for storage: {comp}',
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
    chat_id = get_id(update)

    #Gets user`s company
    user = Profile.objects.filter(external_id = chat_id).get()
    comp_obj = Profile._meta.get_field('company')
    user_comp = getattr(user, comp_obj.attname)

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

    elif b_type == Company:
        for item in items_db:
            if  item.name == user_comp:
                buttons.append(KeyboardButton(text = item.name))
    else:
        for item in items_db:
            buttons.append(KeyboardButton(text = item.name))
    
    update.message.reply_text(
            text = 'List: ',
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
            text = f"Name: {company_id.name} \n Region: {company_id.region} \n City: {company_id.city} \n Address: {company_id.adress} \n Phone: +{company_id.phone}",
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
        chat_id = update.effective_message.chat_id
        update.message.reply_text(
            text = f"Name: {storage_id.name} \n Address: {storage_id.adress} \n Location:",
            reply_markup = ReplyKeyboardMarkup(
                keyboard = [
                    [
                        KeyboardButton(text = button_back),
                    ],
                ],
                resize_keyboard=True
            )
        )
        #Отправляет локацию склада
        bot.send_location(chat_id = chat_id ,latitude = storage_id.latitude, longitude = storage_id.longitude)
        


# Создание инлайн клавиатуры в отдельной функции, чтобы потом навесить её на любое сообщение
def base_inline_keyboard():

    products_db = Product.objects.all()
    for product in products_db:
        if product.name == prod_id.name and product.company == company_id and product.storage == storage_id:
            BTNS={
                BTN_PROD: f'{product.amount} available',
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
        [
            InlineKeyboardButton(BTNS[BTN_SEND], callback_data = BTN_SEND),
        ]
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

    # Записывает роль юзера для дальнейшей проверки
    profiles_db = Profile.objects.filter(external_id = chat_id)
    for item in profiles_db:
        user_role = item.role
        user_company = item.company
        user_id = item.external_id

    def user_change_amount():
        profiles_db = Profile.objects.filter(external_id = chat_id)
        for item in profiles_db:
            user_change = float(item.change_amount)

        return user_change

    def user_change_prod():
        profiles_db = Profile.objects.filter(external_id = chat_id)
        for item in profiles_db:
            prod_change = str(item.change_prod)

        return prod_change

    def changes_to(value, way):
        if way == 'change':
            Profile.objects.filter(external_id = user_id).update(change_amount = (float(user_change_amount())+float(value)))
        else:
            Profile.objects.filter(external_id = user_id).update(change_amount = 0)

    def message_change():
         query.edit_message_text(
                text=f'You want to change {user_change_prod()} by ({user_change_amount()} {prod_id.measurement})',
                reply_markup=base_inline_keyboard(),
                )
    
    def callback_warn():
        query.answer('You don`t have permission.\n(Inappropriate role/Not your company`s storage)', True)

    if data == BTN_PLUS:
        if (user_role == user_roles[0] or user_role == user_roles[2]) and str(user_company) == str(company_id):
            changes_to(1, 'change')
            message_change()
        else:
            callback_warn()

    if data == BTN_MINUS:
        if (user_role == user_roles[0] or user_role == user_roles[1]) and str(user_company) == str(company_id):
            changes_to(-1, 'change')
            message_change()
        else: 
            callback_warn()

    if data == BTN_SEND:
        a, _ = Applications.objects.get_or_create(
            user_id = chat_id,
            company = company_id,
            storage = storage_id,
            product = user_change_prod(),
            amount = user_change_amount(),
            status = 'Waiting'
            )

        query.edit_message_text(
            text = f'Application sent!',
        )
        
        #Обнуляем счётчит количества
        changes_to(0,'set_0')
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
            global prod_id
            prod_id = product
            Profile.objects.filter(external_id = get_id(update)).update(change_prod = str(product))

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
        text = 'Hello there, choose company:',
        reply_markup = reply_markup,
    )

    Profile.objects.filter(external_id = get_id(update)).update(change_amount = 0)

# Связь с джанго через команду
class Command(BaseCommand):
    help = 'Storage Bot'

    def handle(self, *args, **kwargs):
        global bot
        updater = Updater(
            token = TOKEN,
            use_context = True,
        )
        bot = Bot(
            token = TOKEN,
        )

        updater.dispatcher.add_handler(MessageHandler(filters = Filters.all, callback = message_handler, run_async = True))
        updater.dispatcher.add_handler(CallbackQueryHandler(callback=keyboard_callback_handler, run_async = True))

        updater.start_polling()
        updater.idle()


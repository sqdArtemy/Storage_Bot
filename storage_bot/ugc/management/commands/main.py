from os import name
from re import U

from telegram import choseninlineresult

from storage_bot.settings import TOKEN
from telegram.ext import *
from telegram import *

from django.core.management.base import BaseCommand
from ugc.models import Applications, Profile, Company, Storage, Category, Product

# buttons presets
button_companies = 'Companies 🏢'
button_storages = 'Storages🏗️'
button_categories  = 'Categories📑'
button_products = 'Products 📦'
button_info_c = 'Info about Comapany 💡'
button_info_s = 'Info about Storage 💡'
button_back = 'Back 🔙'

# buttons for changing quantity
BTN_PLUS = "callback+"
BTN_MINUS = "callback-"
BTN_PROD = "empty_callback"
BTN_SEND = "send_request"

user_roles = ['Admin', 'Lab', 'S-Manager']

#getting current user`s id
def get_id(update: Update):
    chat_id = update.effective_message.chat_id
    return chat_id

# getting needed item from database
def get_item(update: Update, id, item):
    user = Profile.objects.filter(external_id = id).get()
    field_object = Profile._meta.get_field(str(item))
    choosen_item = getattr(user, field_object.attname)
    
    if item == 'company':
        obj = Company
    elif item == 'selected_storage':
        obj = Storage
    elif item == 'change_prod':
        obj = Product
    else:
        return choosen_item

    #for cases, when we need to take info about particular company or storage
    #because in that case you need an obj, not a string
    db_objects = obj.objects.all()
    for itm in db_objects:
        if choosen_item == itm.name:
            choosen_item = itm

    return choosen_item

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

    # Собирает всю информацию со всех едениц, опять же, зависит от того, какую категорию мы выбираем
    items_db = b_type.objects.all()

    # Проверяет принадлежит ли единица к выбранной компании
    if b_type == Storage:
        for item in items_db:
            if str(get_item(update, get_id(update), 'company')) == str(item.company):
                buttons.append(KeyboardButton(text = item.name))

    elif b_type == Product:
        for item in items_db:
            if str(get_item(update, get_id(update), 'company')) == str(item.company) and str(get_item(update, get_id(update), 'selected_storage')) == str(item.storage) and categ_id == item.category:
                buttons.append(KeyboardButton(text = item.name))

    elif b_type == Company:
        for item in items_db:
            if str(item.name) == str(get_item(update, get_id(update), 'company')):
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
        comp = get_item(update, get_id(update), 'company')
        update.message.reply_text(
            text = f"Name: {comp.name} \n Region: {comp.region} \n City: {comp.city} \n Address: {comp.adress} \n Phone: +{comp.phone}",
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
        storage = get_item(update, get_id(update), 'selected_storage')
        chat_id = update.effective_message.chat_id
        update.message.reply_text(
            text = f"Name: {storage.name} \n Address: {storage.adress} \n Location:",
            reply_markup = ReplyKeyboardMarkup(
                keyboard = [
                    [
                        KeyboardButton(text = button_back),
                    ],
                ],
                resize_keyboard=True
            )
        )
        #Sends storage`s location
        bot.send_location(chat_id = chat_id ,latitude = storage.latitude, longitude = storage.longitude)
        


# Создание инлайн клавиатуры в отдельной функции, чтобы потом навесить её на любое сообщение
def base_inline_keyboard(update: Update):
    storage = get_item(update, get_id(update), 'selected_storage')
    product = get_item(update, get_id(update), 'change_prod')
    company = get_item(update, get_id(update), 'company')

    products_db = Product.objects.all()
    for item in products_db:
        if item.name == product.name and str(item.company) == str(company) and str(item.storage) == str(storage):
            BTNS={
                BTN_PROD: f'{item.amount} available',
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
        reply_markup = base_inline_keyboard(update)
    )

# Обработка всех инлайн кнопок 
def keyboard_callback_handler(update: Update, context: CallbackContext):

    chat_id = update.effective_message.chat_id
    query = update.callback_query
    data = query.data
    product = get_item(update, get_id(update), 'change_prod')

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

    def changes_to(value, way):
        if way == 'change':
            Profile.objects.filter(external_id = user_id).update(change_amount = (float(user_change_amount())+float(value)))
        else:
            Profile.objects.filter(external_id = user_id).update(change_amount = 0)

    def message_change():
         query.edit_message_text(
                text=f'You want to change {str(get_item(update, get_id(update), "change_prod"))} by ({user_change_amount()} {product.measurement})',
                reply_markup=base_inline_keyboard(update),
                )
    
    def callback_warn():
        query.answer('You don`t have permission.\n(Inappropriate role/Not your company`s storage)', True)

    if data == BTN_PLUS:
        if (user_role == user_roles[0] or user_role == user_roles[2]) and str(user_company) == str(get_item(update, get_id(update), 'company')):
            changes_to(1, 'change')
            message_change()
        else:
            callback_warn()

    if data == BTN_MINUS:
        if (user_role == user_roles[0] or user_role == user_roles[1]) and str(user_company) == str(get_item(update, get_id(update), 'company')):
            changes_to(-1, 'change')
            message_change()
        else: 
            callback_warn()

    if data == BTN_SEND:
        a, _ = Applications.objects.get_or_create(
            user_id = chat_id,
            company = get_item(update, get_id(update), 'company'),
            storage = get_item(update, get_id(update), 'selected_storage'),
            product = product,
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
            return menu(update = update, comp = company, m_type = 'companies')

    storages_db = Storage.objects.all()
    for storage in storages_db:
        if text == storage.name:
            Profile.objects.filter(external_id = get_id(update)).update(selected_storage = str(storage))
            return menu(update = update, comp = get_item(update, get_id(update), 'selected_storage'), m_type = 'storages')

    categories_db = Category.objects.all()
    for category in categories_db:
        if text == category.name:
            global categ_id
            categ_id = category

            return selection(update, Product)

    products_db = Product.objects.all()
    for product in products_db:
        if text == product.name:
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
        text = 'Hello there 👋, choose company:',
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
from re import U
from typing import KeysView
from storage_bot.settings import TOKEN
from telegram.ext import *
from telegram import *
from ugc.models import Applications, Profile, Company, Storage, Category, Product

# buttons presets
button_companies = 'Companies 🏢'
button_storages = 'Storages🏗️'
button_categories = 'Categories📑'
button_products = 'Products 📦'
button_info_c = 'Info about Comapany 💡'
button_info_s = 'Info about Storage 💡'
button_back = 'Back 🔙'
button_add_p = 'Add product🆕'

# buttons for changing quantity
BTN_PLUS = "callback+"
BTN_MINUS = "callback-"
BTN_PROD = "empty_callback"
BTN_SEND = "send_request"
BTN10_PLUS = "10plus",
BTN10_MINUS = "10minus",

user_roles = ['Admin', 'Lab', 'S-Manager']


# getting current user`s id
def get_id(update: Update):
    chat_id = update.effective_message.chat_id
    return chat_id


# getting needed item from database
def get_item(update: Update, id, item):
    user = Profile.objects.filter(external_id=id).get()
    field_object = Profile._meta.get_field(str(item))
    choosen_item = getattr(user, field_object.attname)

    if item == 'company':
        obj = Company
    elif item == 'selected_storage':
        obj = Storage
    elif item == 'change_prod':
        obj = Product
    elif item == 'selected_category':
        obj = Category
    else:
        return choosen_item

    # for cases, when we need to take info about particular company or storage
    # because in that case you need an obj, not a string
    db_objects = obj.objects.all()
    for itm in db_objects:
        if obj == Category and choosen_item == itm.id:
            choosen_item = itm
        if choosen_item == itm.name:
            choosen_item = itm

    return choosen_item


# gives information about how to form panel after 'back' button have been pressed #WIP
def selected_page(update: Update, page):
    chat_id = get_id(update)
    user = Profile.objects.filter(external_id=chat_id).get()
    target = Profile._meta.get_field('current_page')
    cur_button = getattr(user, target.attname)-1

    if page-1 >= 0:
        Profile.objects.filter(external_id=chat_id).update(
            previous_page=page - 1)
        Profile.objects.filter(external_id=chat_id).update(current_page=page)
        return page - 1
    else:
        return 0


# displays button menu in ralation with selected category
def menu(update: Update, comp, m_type):
    buttons = []

    if m_type == 'companies':  # button layout for companies
        text = f'Menu for company: {comp}'
        buttons.append(KeyboardButton(text=button_storages))
        buttons.append(KeyboardButton(text=button_info_c))

    if m_type == 'storages':  # button layout for storages
        text = f'Menu for storage: {comp}'
        buttons.append(KeyboardButton(text=button_categories))
        buttons.append(KeyboardButton(text=button_info_s))

    Keyboard = [buttons, [KeyboardButton(text=button_back)]]

    update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=Keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        )
    )


# creates buttons with respect to selected category
def selection(update: Update, b_type):
    buttons = []
    chat_id = get_id(update)

    # collects all info about seected object
    items_db = b_type.objects.all()

    # checks wheter item belongs to company
    if b_type == Storage:
        for item in items_db:
            if str(get_item(update, chat_id, 'company')) == str(item.company):
                buttons.append(KeyboardButton(text=item.name))

    elif b_type == Product:
        for item in items_db:
            if str(get_item(update, chat_id, 'company')) == str(item.company) and str(get_item(update, chat_id, 'selected_storage')) == str(item.storage) and categ_id == item.category:
                buttons.append(KeyboardButton(text=item.name))

    elif b_type == Company:
        for item in items_db:
            if str(item.name) == str(get_item(update, chat_id, 'company')):
                buttons.append(KeyboardButton(text=item.name))
    else:
        for item in items_db:
            buttons.append(KeyboardButton(text=item.name))

    # adds additional button if particular type is selected
    if b_type == Product:
        Keyboard = [buttons, [KeyboardButton(
            text=button_back), KeyboardButton(text=button_add_p), ]]

    else:
        Keyboard = [buttons, [KeyboardButton(text=button_back)]]

    update.message.reply_text(
        text='List 📝 ',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=Keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


# displays info about company or storage
def info_about(update: Update, inf):
    Keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=button_back)],
        ],
        resize_keyboard=True
    )

    if inf == Company:
        comp = get_item(update, get_id(update), 'company')
        update.message.reply_text(
            text=f"Name: {comp.name} \n Region: {comp.region} \n City: {comp.city} \n Address: {comp.adress} \n Phone: +{comp.phone}",
            reply_markup=Keyboard
        )
    elif inf == Storage:
        bot = Bot(token=TOKEN)
        storage = get_item(update, get_id(update), 'selected_storage')
        chat_id = update.effective_message.chat_id
        update.message.reply_text(
            text=f"Name: {storage.name} \n Address: {storage.adress} \n Location:",
            reply_markup=Keyboard
        )
        # sends storage`s location
        bot.send_location(
            chat_id=chat_id, latitude=storage.latitude, longitude=storage.longitude)


# inline keyboard for changing amount of prduct
def base_inline_keyboard(update: Update, type_p):
    storage = get_item(update, get_id(update), 'selected_storage')
    product = get_item(update, get_id(update), 'change_prod')
    company = get_item(update, get_id(update), 'company')

    if type_p == 'change':
        products_db = Product.objects.all()
        for item in products_db:
            if item.name == product.name and str(item.company) == str(company) and str(item.storage) == str(storage):
                BTNS = {
                    BTN_PROD: f'{item.amount} available',
                    BTN_PLUS: "➕",
                    BTN_MINUS: "➖",
                    BTN_SEND: "Send➡️",
                    BTN10_PLUS: "10➕",
                    BTN10_MINUS: "10➖",
                }

                keyboard = [
                    [InlineKeyboardButton(
                        BTNS[BTN_PROD], callback_data=BTN_PROD), ],
                    [
                        InlineKeyboardButton(
                            BTNS[BTN_PLUS], callback_data=BTN_PLUS),
                        InlineKeyboardButton(
                            BTNS[BTN_MINUS], callback_data=BTN_MINUS),
                    ],
                    [InlineKeyboardButton(
                        BTNS[BTN_SEND], callback_data=BTN_SEND), ]
                ]
    elif type_p == 'create':
        BTNS = {
            BTN_PLUS: "➕",
            BTN_MINUS: "➖",
            BTN_SEND: "Send➡️",
            BTN10_PLUS: "10➕",
            BTN10_MINUS: "10➖",
        }

        keyboard = [
            [
                InlineKeyboardButton(BTNS[BTN10_PLUS], callback_data='set+10'),
                InlineKeyboardButton(BTNS[BTN_PLUS], callback_data="set+1"),
                InlineKeyboardButton(BTNS[BTN_MINUS], callback_data="set-1"),
                InlineKeyboardButton(
                    BTNS[BTN10_MINUS], callback_data='set-10'),
            ],
            [InlineKeyboardButton(BTNS[BTN_SEND], callback_data='send'), ]
        ]

    return InlineKeyboardMarkup(keyboard)


# displays menu with adjusted changes of product
def product_adjustments(update, prod):
    update.message.reply_text(
        text=f'{prod.name} ({prod.measurement})',
        reply_markup=base_inline_keyboard(update, 'change')
    )


# handles callbacks from all inline buttons
def keyboard_callback_handler(update: Update, context: CallbackContext):

    chat_id = update.effective_message.chat_id
    query = update.callback_query
    data = query.data
    product = get_item(update, get_id(update), 'change_prod')

    # Записывает роль юзера для дальнейшей проверки
    profiles_db = Profile.objects.filter(external_id=chat_id)
    for item in profiles_db:
        user_role = item.role
        user_company = item.company
        user_id = item.external_id

    def user_change_amount():
        profiles_db = Profile.objects.filter(external_id=chat_id)
        for item in profiles_db:
            user_change = float(item.change_amount)
        return user_change

    def changes_to(value, way):
        if way == 'change':
            Profile.objects.filter(external_id=user_id).update(
                change_amount=(float(user_change_amount())+float(value)))
        else:
            Profile.objects.filter(external_id=user_id).update(change_amount=0)

    def message_change():
        query.edit_message_text(
            text=f'You want to change {str(get_item(update, get_id(update), "change_prod"))} by ({user_change_amount()} {product.measurement})',
            reply_markup=base_inline_keyboard(update, 'change'),
        )

    def message_add():
        query.edit_message_text(
            text=f'Entered amount:  {get_item(update, get_id(update), "change_amount")} 📝',
            reply_markup=base_inline_keyboard(update, 'create')
        )

    def callback_warn():
        query.answer(
            'You don`t have permission.\n(Inappropriate role/Not your company`s storage)', True)

    if data == BTN_PLUS:
        if (user_role == user_roles[0] or user_role == user_roles[1]) and str(user_company) == str(get_item(update, get_id(update), 'company')):
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
            user_id=chat_id,
            company=get_item(update, get_id(update), 'company'),
            storage=get_item(update, get_id(update), 'selected_storage'),
            product=product,
            amount=user_change_amount(),
            status='Waiting'
        )

        query.edit_message_text(
            text=f'Application sent!',
        )

        # sets g page to the initial condition
        Profile.objects.filter(external_id=chat_id).update(
            previous_page=0, current_page=0)

        # sets counter to 0
        changes_to(0, 'set_0')

    if data == 'send':
        name = get_item(update, chat_id, 'create_name')
        comp = get_item(update, chat_id, 'company').name
        stor = get_item(update, chat_id, 'selected_storage').name
        change_amount = get_item(update, chat_id, 'change_amount')

        Product.objects.filter(name=name, storage=stor,
                               company=comp).update(amount=change_amount)
        query.edit_message_text(text='Changes saved!✅')
        Profile.objects.filter(external_id=chat_id).update(change_amount=0)

    call_back = data.split('-')  # splits callback to 2 parts
    if len(call_back) >= 2 and (call_back[0] == "YES" or call_back[0] == "NO"):

        def already_reacted():
            query.answer('Application was already handled!')

        application = Applications.objects.filter(
            id=int(call_back[1])).last()  # getting application from DB
        if call_back[0] == 'YES' and application.status == 'Waiting':
            query.edit_message_text(text='Application accepted!✅')

            application.status = 'Accepted'
            application.save()

        elif call_back[0] == 'NO' and application.status == 'Waiting':
            query.edit_message_text(text='Aplication discarded!❌')

            application.status = 'Denied'
            application.save()
        else:
            already_reacted()
            query.delete_message()

    if data == 'set+10':
        changes_to(10, 'change')
        message_add()

    if data == 'set-10':
        changes_to(-10, 'change')
        message_add()

    if data == 'set+1':
        changes_to(1, 'change')
        message_add()

    if data == 'set-1':
        changes_to(-1, 'change')
        message_add()

    else:
        pass


# create new product
def create_prod(update: Update):
    chat_id = get_id(update)
    prod_name = get_item(update, chat_id, 'create_name')
    p, _ = Product.objects.get_or_create(
        company=get_item(update, chat_id, 'company'),
        storage=get_item(update, chat_id, 'selected_storage'),
        category=get_item(update, chat_id, 'selected_category'),
        name=prod_name,
        measurement=get_item(update, chat_id, 'change_measurement'),
        amount=0)

    update.message.reply_text(
        text=f'You have added new product: {prod_name}! Now enter quantity',
        reply_markup=base_inline_keyboard(update, 'create')
    )

    Profile.objects.filter(external_id=chat_id).update(state='default')


# handles all messages from the user
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    chat_id = update.message.chat_id
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_companies),
            ],
        ],
        resize_keyboard=True
    )

    # adds users to profile
    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
    )

    # cheks for keywords
    if text == button_companies:
        selected_page(update, 1)
        return selection(update, Company)

    elif text == button_storages:
        selected_page(update, 3)
        return selection(update, Storage)

    elif text == button_categories:
        selected_page(update, 5)
        return selection(update, Category)

    elif text == button_info_s:
        selected_page(update, 4)
        return info_about(update=update, inf=Storage)

    elif text == button_info_c:
        selected_page(update, 2)
        return info_about(update=update, inf=Company)

    # if user wants to create new item - ask name of it
    if text == button_add_p:
        update.message.reply_text(
            text='Please, enter products name: ',
        )
        Profile.objects.filter(external_id=get_id(
            update)).update(state='prod_name')

    # assign name and ask measurement
    elif get_item(update, chat_id, 'state') == 'prod_name':
        Profile.objects.filter(external_id=chat_id).update(
            create_name=update.message.text)
        Profile.objects.filter(external_id=chat_id).update(
            state='prod_measure')

        update.message.reply_text(
            text='Please, enter products measurement: ',
        )

    # then writes the measurement and add it to database
    elif get_item(update, chat_id, 'state') == 'prod_measure':
        Profile.objects.filter(external_id=chat_id).update(
            change_measurement=update.message.text)
        Profile.objects.filter(external_id=chat_id).update(state='default')
        create_prod(update)

    elif text == button_back:
        update.message.reply_text(
            text='Hello there 👋, choose company:',
            reply_markup=reply_markup,
        )

    companies_db = Company.objects.all()
    for company in companies_db:
        if text == company.name:
            return menu(update=update, comp=company, m_type='companies')

    storages_db = Storage.objects.all()
    for storage in storages_db:
        if text == storage.name:
            Profile.objects.filter(external_id=get_id(update)).update(
                selected_storage=str(storage))
            return menu(update=update, comp=get_item(update, get_id(update), 'selected_storage'), m_type='storages')

    categories_db = Category.objects.all()
    for category in categories_db:
        if text == category.name:
            global categ_id
            categ_id = category
            Profile.objects.filter(external_id=chat_id).update(
                selected_category=category)

            return selection(update, Product)

    products_db = Product.objects.all()
    for product in products_db:
        if text == product.name:
            Profile.objects.filter(external_id=get_id(
                update)).update(change_prod=str(product))

            return product_adjustments(update, product)

    Profile.objects.filter(external_id=get_id(update)).update(change_amount=0)


# start command
def start(update: Update, context):
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button_companies),
            ],
        ],
        resize_keyboard=True
    )
    update.message.reply_text(
        text='Hello there 👋, choose company:',
        reply_markup=reply_markup,
    )

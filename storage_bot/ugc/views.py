from telegram import *
from telegram.bot import Bot
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.dispatcher import Dispatcher
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from ugc.management.commands.main import keyboard_callback_handler, message_handler, start
from storage_bot.settings import TOKEN
from django.http import JsonResponse
from rest_framework.views import APIView
from telegram.ext import Updater
import os

# Create your views here.
class Test(APIView):
    def post(self, request, *args, **options):

        PORT = int(os.environ.get('PORT', '8000'))

        bot = Bot(token = TOKEN)
        dispatcher = Dispatcher(bot, None, workers=6)

        #THIS WHOLE THING FOR SETTING WEBHOOK
        # url = "https://6be2-213-230-127-84.ngrok.io/" #web-app link

        # bot.setWebhook(url + 'storage/')

        # updater = Updater(
        #     bot = bot,
        #     use_context = True,
        # )

        # updater.start_webhook(listen="0.0.0.0",
        #     port=PORT,
        #     url_path=TOKEN,
        #     webhook_url=(url+'storage/'))

        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(MessageHandler(filters = Filters.all, callback = message_handler))
        dispatcher.add_handler(CallbackQueryHandler(callback=keyboard_callback_handler))

        dispatcher.process_update( Update.de_json(request.data, bot))
        return JsonResponse({"ok": "POST request processed"})

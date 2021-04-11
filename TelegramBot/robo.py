TOKEN1="1180305025:AAGrfeE2pLN9_ktB70up0HYwBocFWgvTbp4"
TOKEN2="840809150:AAH20Hy4EMl68cf8YvP0AsOilnGCf1cZpNc"

import logging
import asyncio
import queue

### mac adrese blutuutha

## i  :  48:87:2D:12:8B:30
## ii :  48:87:2D:12:93:A5
## iii:  48:87:2D:12:92:20
MAC="48:87:2D:12:92:20"
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("f=foward, b=back, l=left, r=right, a=LED")


def echo(update, context):
    """Echo the user message."""
    #update.message.reply_text(update.message.text)
    c=update.message.text.lower()
    if c in ['f', 'b', 'l','r','a']:
        q.put(c)
    

def start(update, context):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))



def telegram_bot():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN2, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    #updater.dispatcher.add_handler(CallbackQueryHandler(button))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    try:
        updater.start_polling()
    except KeyboardInterrupt:
        updater.stop()

    print("kek")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    #updater.idle()

    #print("like do something")


from bleak import BleakClient
from bleak import _logger as logger
from bleak.uuids import uuid16_dict
from array import array

IO_DATA_CHAR_UUID = "0000ffe2-0000-1000-8000-00805f9b34fb"

async def connect_to_robot(address):
    client = BleakClient(address, timeout=1.0)
    x = await client.connect()
    print("Connected: {0}".format(x))


async def send_character(address):
    client = BleakClient(address, timeout=1.0)
    x = await client.connect()
    print("Connected: {0}".format(x))

    while True:
        c = q.get(timeout=None)
        b=bytearray(c, 'ascii')
        await client.write_gatt_char(IO_DATA_CHAR_UUID, b)
        q.task_done()


async def main():
    #q=asyncio.Queue()
    telegram_bot()
    #client = await connect_to_robot(address)
    tasks=asyncio.create_task(send_character(address))
    #s=asyncio.create_task(telegram_bot(client))
    #cmd=asyncio.create_task(cmd_input(q))
    await asyncio.gather(tasks)
    print("created tasks")
    

q = queue.Queue()
if __name__ == '__main__':
    import os
    #
    print("START")
    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    address = MAC
    try:
        asyncio.run(main())
    finally:
        print("END")


from xml.dom import NoDataAllowedErr
import Constants as keys
from telegram import Bot, Update , BotCommand, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import Responses as R
import Contract 
from datetime import datetime 
import time
import threading

dp = None
updateTimer = None
lastTimerMesage = 0
print("bot started...")


def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator

def start_command(update,context):
  update.message.reply_text('type somthings random to get started!')

def handle_message(update, context):
  text = str(update.message.text).lower()
  response = R.sample_responses(text)

  update.message.reply_text(response)

def help_command(update,context):
  update.message.reply_text('If you need help ask the Guardian team!')

def lastwon_command(update,context):
  update.message.reply_text(Contract.lastAwarded())


def lastbuy_command(update,context):
  update.message.reply_text(Contract.lastBuy())


def bigbang_command(update,context):
  update.message.reply_text(Contract.lastBigBang())


def guardpot_command(update,context):
  update.message.reply_text(Contract.guardPot())

   
@setInterval(5)
def send_update(bot):
  global lastTimerMesage

  result =  bot.sendMessage(chat_id="@guardian_token", text=Contract.guardTimer())
  if(lastTimerMesage != 0):
    bot.deleteMessage("@guardian_token", lastTimerMesage)
    
  lastTimerMesage = result["message_id"]

def main():
  updater = Updater(keys.API_KEY, use_context=True)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler('start', start_command))
  dp.add_handler(CommandHandler('help', help_command))
  dp.add_handler(CommandHandler('bigcrunch', bigbang_command))
  dp.add_handler(CommandHandler('lastwon', lastwon_command))
  dp.add_handler(CommandHandler('guardbuy', lastbuy_command))
  dp.add_handler(CommandHandler('guardpot', guardpot_command))
  dp.add_handler(CommandHandler('contract', handle_message))
  dp.add_handler(CommandHandler('ca', handle_message))
  dp.add_handler(CommandHandler('chart', handle_message))
  dp.add_handler(CommandHandler('buy', handle_message))
  # dp.add_handler(CommandHandler('timer', timer_command))
  # dp.add_handler(CommandHandler('stoptimer', stop_timer_command))

  dp.bot.set_my_commands([
    BotCommand("bigcrunch","Show the last BIG Crunch stats"),
    BotCommand("guardbuy","Show the last guardian angel buy"),
    BotCommand("lastwon","Show the last GuardPot awarded"),
    BotCommand("guardpot","Show the current GuardPot informations"),
    BotCommand("contract","Get the official GUARD contract"),
    BotCommand("chart","Get the chart link"),
    BotCommand("buy","Buy GUARD token throw pancakeswap")

  ])
  
  bot = Bot(token=keys.API_KEY)
  updateTimer = send_update(bot) # start timer, the first call is in .5 seconds
  # updateTimer.set() #stop the timer

  # dp.add_error_handler(error)
  updater.start_polling(0)
  
  updater.idle()


main()

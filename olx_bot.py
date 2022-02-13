import logging
import telegram
import config
from telegram.ext import messagequeue as mq
from telegram import InputMediaPhoto, ParseMode, InlineKeyboardMarkup, Update, replymarkup, update, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, error
from telegram.ext import JobQueue,Updater, CommandHandler, MessageHandler, Filters, callbackcontext, CallbackQueryHandler,ConversationHandler, commandhandler


from get_web import get_adverts
SEARCHTEXT, SENDADV, SENDV = range(3)

i=0




logging.basicConfig(format='%(asctime)s - %(levelname)s -%(message)s',
level=logging.INFO,
filename='bot.log'
)

def start(update,context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Введите поисковый запрос")
    return SEARCHTEXT






def searchtext(update,context):
    global search_text
    search_text = update.message.text
    reply_keyboard = ReplyKeyboardMarkup([['Oтправить обьявления'],['Переписать запрос']], one_time_keyboard = True, resize_keyboard = True)
    context.bot.send_message(chat_id = update.effective_chat.id, text = f'Ваш поисковый запрос: {search_text}',reply_markup = reply_keyboard)
    return SENDV
    



def sendv(update,context):
   
    global adverts
    adverts = get_adverts(f'https://www.olx.ua/list/q- {search_text}')
    
    single_adv=adverts[0]
    text = """
<b>{title}</b> 
<i>Цена:</i> <b>{price}</b>
<i>Город:</i> <b>{location}</b>
<b>{url}</b>

<b>Для повторного поиска введите поисковый запрос</b>
""".format(**single_adv)
    klava = [
        [InlineKeyboardButton('Вперед',callback_data='1')],
        [InlineKeyboardButton('Назад',callback_data='2')]
  
    ]
    reply_markup = InlineKeyboardMarkup(klava)
    context.bot.send_photo(chat_id = update.effective_chat.id, photo=single_adv['img'], caption = text,   parse_mode = ParseMode.HTML, reply_markup = reply_markup)
    return SENDADV

def send_advert(update,context):
    global i
    query = update.callback_query
    c = query.data
    
    single_adv=adverts[i]
    text = """
<b>{title}</b> 
<i>Цена:</i> <b>{price}</b>
<i>Город:</i> <b>{location}</b>
<b>{url}</b>

<b>Для повторного поиска введите поисковый запрос</b>
""".format(**single_adv)
    klava = [
    [InlineKeyboardButton('Вперед',callback_data='1')],
    [InlineKeyboardButton('Назад',callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(klava)
  
    if c == '1':
        i = i+1
        single_adv=adverts[i]
        update.edit_message_media(
                media = InputMediaPhoto(
                    media = single_adv['img'],
                    caption=text,
                    parse_mode=ParseMode.HTML
                    ),
                reply_markup=reply_markup
                )
       
    if c == '2':
        i =  i - 1
        single_adv=adverts[i]
        update.edit_message_media(
                media = InputMediaPhoto(
                    media = single_adv['img'],
                    caption=text,
                    parse_mode=ParseMode.HTML
                    ),
                reply_markup=reply_markup
                )

    
def main():

    mybot = Updater("1862999216:AAHY1Tvkx0muNVuksrvWYEokOn4xqxZw8wQ")
    
    logging.info('Bot is started')
    dp= mybot.dispatcher
    opros = ConversationHandler(
        entry_points = [CommandHandler('start',start)],
        states ={
            SEARCHTEXT:[MessageHandler(Filters.text,searchtext)],
            SENDADV:[CallbackQueryHandler(send_advert)],
            SENDV:[MessageHandler(Filters.regex('^Oтправить обьявления$'), sendv)]
        },
        fallbacks = [MessageHandler(Filters.command ('start'),start),MessageHandler(Filters.regex('^Переписать запрос$'), start),MessageHandler(Filters.text, searchtext)]
     
    )
    dp.add_handler(opros)



    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()
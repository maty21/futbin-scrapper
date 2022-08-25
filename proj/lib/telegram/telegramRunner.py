print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
from telegram import Update,InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,InlineQueryHandler ,MessageHandler ,filters
from telegram.constants import ParseMode
from html import escape
from uuid import uuid4
from proj.lib.playerQuerier import PlayerQuerier
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class TelegramRunner:
            
    def __init__(self):
        self.app= None
        self._pq = PlayerQuerier()
        self._pq.init()
        
    async def hello(self,update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f'Hello {update.effective_user.first_name}')

    async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

    async def inline_caps(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.inline_query.query
        if len(query) < 4:
            await update.inline_query.answer([])
            return
        else:
            res = self._pq.findPlayerData(query)
            if len(res)>0:
                results = [
                            InlineQueryResultArticle(
                            id=f'found {len(res)} amount sending result for {res[0][1]}',
                            title='PRICE',
                            input_message_content=InputTextMessageContent(f'found {len(res)} amount sending result for {res[0][1]} = {res[0][8]}' )),
                            
                            # InlineQueryResultArticle(
                            # id=str(uuid4()),
                            # title="Caps",
                            # input_message_content=InputTextMessageContent(query.upper())),
                            
                            InlineQueryResultArticle(
                                id=str(uuid4()),
                                title="Bold",
                                input_message_content=InputTextMessageContent(
                                    f"<b>{escape(query)}</b>", parse_mode=ParseMode.HTML
                                ),
                                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("test", callback_data="test")]])),
                            
                            # InlineQueryResultArticle(
                            #     id=str(uuid4()),
                            #     title="Italic",
                            #     input_message_content=InputTextMessageContent(
                            #         f"<i>{escape(query)}</i>", parse_mode=ParseMode.HTML),
                            # ),
                    ]
                await context.bot.answer_inline_query(update.inline_query.id, results)     
            else:
                sq = query.split(" ")
                if sq[0] == "price":
                    res= self._pq.findPlayerIdByDetails(name=sq[1],rating=sq[2])
                    results = [
                                InlineQueryResultArticle(
                                id=str(uuid4()),
                                title="Caps",
                                input_message_content=InputTextMessageContent(query.upper()),
                            ),
                            InlineQueryResultArticle(
                                id=str(uuid4()),
                                title="Bold",
                                input_message_content=InputTextMessageContent(
                                    f"<b>{escape(query)}</b>", parse_mode=ParseMode.HTML
                                ),
                            ),
                            InlineQueryResultArticle(
                                id=str(uuid4()),
                                title="Italic",
                                input_message_content=InputTextMessageContent(
                                    f"<i>{escape(query)}</i>", parse_mode=ParseMode.HTML
                                ),
                            ),
                    ]
                    results.append(
                        InlineQueryResultArticle(
                            id=sq[0]+"/"+sq[1],
                            title='PRICE',
                            input_message_content=InputTextMessageContent(res[0][8])
                        )
                    )
                await context.bot.answer_inline_query(update.inline_query.id, results)
                
    def runner(self):
        self.app = ApplicationBuilder().token("token").build()
        self.app.add_handler(CommandHandler("hello", self.hello))
        self.app.add_handler(InlineQueryHandler(self.inline_caps))
        unknown_handler = MessageHandler(filters.COMMAND, self.unknown)
        self.app.add_handler(unknown_handler)
        self.app.run_polling()
        
        

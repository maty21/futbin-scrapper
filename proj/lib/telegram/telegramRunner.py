print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
from telegram import Update,InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,InlineQueryHandler

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

    async def inline_caps(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.inline_query.query
        if not query:
            return
        else:
            sq = query.split(" ")
            if sq[0] == "price":
                res= self._pq.findPlayerIdByDetails(name=sq[1],rating=sq[2])
                results = []
                results.append(
                    InlineQueryResultArticle(
                        id=sq[0]+"/"+sq[1],
                        title='PRICE',
                        input_message_content=InputTextMessageContent(res[0][8])
                    )
                )
                await context.bot.answer_inline_query(update.inline_query.id, results)
            
    def runner(self):
        self.app = ApplicationBuilder().token("2024197533:AAEe7RVyPXBT8Lt6HTFXFFyNTy9FPtypsv8").build()
        self.app.add_handler(CommandHandler("hello", self.hello))
        self.app.add_handler(InlineQueryHandler(self.inline_caps))
        self.app.run_polling()
        
        

from telegram import Update,InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,InlineQueryHandler
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)
    
    
app = ApplicationBuilder().token("2024197533:AAEe7RVyPXBT8Lt6HTFXFFyNTy9FPtypsv8").build()


app.add_handler(CommandHandler("hello", hello))
app.add_handler(InlineQueryHandler(inline_caps))
app.run_polling()
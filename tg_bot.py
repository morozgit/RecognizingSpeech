import os
from dotenv import load_dotenv, find_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import telegram
from tg_logs_handler import TelegramLogsHandler
from dialogflow_api import detect_intent_texts


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def send_massage(update: Update, context: CallbackContext, project_id):
    texts = update.message.text
    user_id = update.effective_user.id
    answer = detect_intent_texts(project_id, texts, user_id)
    update.message.reply_text(answer.query_result.fulfillment_text)


def main():
    load_dotenv(find_dotenv())
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    project_id = os.environ.get("PROJECT_ID")
    tg_chat_id = os.environ.get("TG_CHAT_ID")
    bot = telegram.Bot(token=tg_token)
    bot.logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))
    bot.logger.warning('Бот запущен')

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    try:
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                              lambda update, context: send_massage(update, context, project_id)))
        updater.start_polling()
        updater.idle()
    except Exception as err:
        error = f'Бот упал с ошибкой {str(err)}'
        bot.logger.warning(error)


if __name__ == '__main__':
    main()
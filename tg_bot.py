import os
from dotenv import load_dotenv, find_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from google.cloud import dialogflow
import logging
import telegram


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def detect_intent_texts(update: Update, context: CallbackContext, project_id, session_id):
    project_id = project_id
    session_id = session_id
    language_code = 'ru'
    texts = update.message.text
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    update.message.reply_text(response.query_result.fulfillment_text)


def main():
    load_dotenv(find_dotenv())
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    project_id = os.environ.get("PROJECT_ID")
    session_id = os.environ.get("SESSION_ID")
    tg_chat_id = os.environ.get("TG_CHAT_ID")
    bot = telegram.Bot(token=tg_token)
    bot.logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))
    bot.logger.warning('Бот запущен')

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    try:
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command,
                                              lambda update, context: detect_intent_texts(update, context, project_id,
                                                                                          session_id)))
        updater.start_polling()
        updater.idle()
    except Exception as err:
        error = f'Бот упал с ошибкой {str(err)}'
        bot.logger.warning(error)


if __name__ == '__main__':
    main()
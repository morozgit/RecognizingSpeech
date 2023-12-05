import os
from dotenv import load_dotenv, find_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from google.cloud import dialogflow


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')


def detect_intent_texts(update: Update, context: CallbackContext):
    project_id = 'recognizingspeech'
    session_id = 'temchmorozov'
    language_code = 'ru'
    texts = update.message.text
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    # for text in texts:
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    update.message.reply_text(response.query_result.fulfillment_text)


def main():
    load_dotenv(find_dotenv())
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, detect_intent_texts))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
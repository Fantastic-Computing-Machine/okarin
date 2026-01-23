import os
import threading
from typing import Optional

from dotenv import load_dotenv
import telebot

from services.chat_service import process_message

load_dotenv()

_bot: Optional[telebot.TeleBot] = None
_polling_thread: Optional[threading.Thread] = None


def get_bot() -> telebot.TeleBot:
    global _bot
    if _bot is None:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in the environment.")

        _bot = telebot.TeleBot(token)
        _register_handlers(_bot)
    return _bot


def _register_handlers(bot: telebot.TeleBot) -> None:
    @bot.message_handler(content_types=["text"])
    def handle_text(message):
        try:
            reply = process_message(message.text or "")
        except Exception as e:
            print(f"Error processing message: {e}")
            reply = "Sorry, something went wrong while processing your message."
        send_message(message.chat.id, reply)


def send_message(chat_id: int | str, text: str) -> None:
    bot = get_bot()
    bot.send_message(chat_id, text)


def start_bot() -> None:
    global _polling_thread
    bot = get_bot()

    if _polling_thread and _polling_thread.is_alive():
        return

    def _poll():
        bot.infinity_polling(timeout=20, long_polling_timeout=10)

    _polling_thread = threading.Thread(
        target=_poll, name="telegram-bot-polling", daemon=True
    )
    _polling_thread.start()


def stop_bot() -> None:
    global _polling_thread
    if _bot:
        _bot.stop_polling()

    if _polling_thread:
        _polling_thread.join(timeout=5)
        _polling_thread = None

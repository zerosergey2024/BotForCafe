import telebot
from telebot import types
import time
import os

from config import TELEGRAM_API_TOKEN



# Путь к изображению кафе
CAFE_PHOTO_PATH = 'cafe_photo.jpg'

class Menu:
    def __init__(self):
        self.last_menu = {}

    def create_menu_keyboard(self, callback):
        # Создание клавиатуры для текущего уровня меню
        markup = types.InlineKeyboardMarkup()






class Messages:
    sent_messages = {}  # Переместили инициализацию переменной выше

    @classmethod
    def save_message_id(cls, user_id, message_id, id):
        """Сохраняет ID сообщения, отправленного ботом, с привязкой к идентификатору."""

        # Проверяем, есть ли уже записи для данного пользователя
        if user_id not in cls.sent_messages:
            cls.sent_messages[user_id] = {}  # Инициализируем словарь для конкретного пользователя

        # Сохраняем id под конкретным message_id
        cls.sent_messages[user_id][message_id] = id

    @classmethod
    def clear_chat_history(cls, user_id):
        """Удаляет все сообщения, отправленные ботом в данном чате."""
        if user_id in cls.sent_messages:
            # Получаем список message_id для удаления
            message_ids = list(cls.sent_messages[user_id].keys())

            for message_id in message_ids:
                try:
                    bot.delete_message(user_id, message_id)
                    time.sleep(0.05)  # Задержка, чтобы избежать лимитов API
                except Exception as e:
                    print(f"Не удалось удалить сообщение {message_id}: {e}")

            # Очистка словаря сообщений после их удаления
            cls.sent_messages[user_id] = {}

    @classmethod
    def send_new_message(cls, user_id, msg_text, image_url, markup_keys, buttons, id, old_message):
        """Отправка сообщения - только текст или текст/картинка + markup_keys
        Сохраняет ID сообщения, отправленного ботом, с привязкой к идентификатору"""
        try:
            if not markup_keys and buttons:
                markup_keys = types.InlineKeyboardMarkup()
                for button in buttons:
                    markup_button = types.InlineKeyboardButton(button["text"], callback_data=button["callback_data"])
                    markup_keys.add(markup_button)

            if not msg_text and old_message and markup_keys: # нет текста - меняем только кнопки у старого сообщения
                bot.edit_message_reply_markup(
                              chat_id=user_id,
                              message_id=old_message.message_id,
                              reply_markup=markup_keys)
                return

            with open(image_url, 'rb') as photo:
                msg = bot.send_photo(
                    user_id,
                    photo,
                    caption=msg_text,
                    reply_markup=markup_keys)
            cls.save_message_id(user_id, msg.message_id, id)
        except (TypeError, FileNotFoundError):
            msg = bot.send_message(
                user_id,
                text=msg_text,
                reply_markup=markup_keys
            )
            cls.save_message_id(user_id, msg.message_id, id)

# Токен вашего бота
bot = telebot.TeleBot(TELEGRAM_API_TOKEN, parse_mode='HTML')

# Создаем экземпляр класса Menu
menu = Menu()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_cafe_menu(message.chat.id)

def send_cafe_menu(chat_id):
    # Создание клавиатуры с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    # Добавление кнопок с иконками
    btn_menu = types.KeyboardButton('🍽️ Меню кафе')
    btn_cart = types.KeyboardButton('🛒 Корзина')
    btn_payment = types.KeyboardButton('💰 Оплата заказа')
    btn_status = types.KeyboardButton('📦 Статус заказа')
    btn_rating = types.KeyboardButton('⭐ Рейтинг')

    markup.add(btn_menu, btn_cart, btn_payment, btn_status, btn_rating)

    # Отправка фото кафе и клавиатуры
    with open(CAFE_PHOTO_PATH, 'rb') as photo:
        bot.send_photo(chat_id, photo, caption="Добро пожаловать в наше кафе!", reply_markup=markup)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):





 print("Bot is running...")

bot.polling()
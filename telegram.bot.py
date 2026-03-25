import telebot
from telebot import types
import random
import requests
import json
from datetime import datetime

TOKEN = "token"

bot = telebot.TeleBot(TOKEN)

main = ["Ножиці папір✂️", "Однорукий бандит✋", "Кубік рубік🎲","💲Курс валют", "🌤️ Погода"]
choice = ["Камінь", "Ножиці", "Папір"]
page_2 = [""]


scores = {}
win_streak = {}
user_gifts = {}
user_caculator = {}



@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        user = message.from_user
        chat = message.chat
        user_id = user.id


        user_gifts[user_id] = "🎁 Есть подарок на аккаунте"
        gift = user_gifts.get(user_id, "Нет подарка")


        premium_status = "Да ⭐" if hasattr(user, 'is_premium') and user.is_premium else "Нет ❌"


        info = f"""
Пользователь нажал /start:
ID: {user.id}
Username: @{user.username if user.username else 'нет'}
First Name: {user.first_name}
Last Name: {user.last_name if user.last_name else 'нет'}
Is bot: {user.is_bot}
Language: {user.language_code if user.language_code else 'не указан'}
Дата/время: {datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')}
Тип чата: {chat.type}
Chat ID: {chat.id}
Premium: {premium_status}
Сообщение: {message.text}
"""
        print(info)


        with open("photo.png", "rb") as photo:
            bot.send_photo(chat.id, photo)
    
        bot.send_message(
            chat.id,
            "Вітаю, вибери одну гру 👇",
            reply_markup=get_keyboard()
        )


    except AttributeError as a:
        print("Что-то поламалось")


def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Ножиці папір✂️", "Однорукий бандит✋", "Кубік рубік🎲", "Вгадай число💌", "💲Курс валют",)
    return keyboard

def kyrs_valut():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("USD 💵", "EUR 💶", "BTC ₿")
    keyboard.add("⬅️ Назад")
    return keyboard

def game_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Камінь", "Ножиці", "Папір")
    keyboard.add("⬅️ Назад")
    return keyboard




@bot.message_handler(func=lambda m: m.text == "Ножиці папір✂️")
def game1(message):

    user_id = message.from_user.id

    if user_id not in scores:
        scores[user_id] = {"user": 0, "bot": 0}
        win_streak[user_id] = 0

    bot.send_message(
        message.chat.id,
        "Гра Камінь Ножиці Папір ✂️\nОбери свій варіант 👇",
        reply_markup=game_keyboard()
    )


@bot.message_handler(func=lambda m: m.text in choice)
def play(message):

    user_id = message.from_user.id
    chat_id = message.chat.id

    user_choice = message.text
    bot_choice = random.choice(choice)

    result = ""

    if user_choice == bot_choice:
        result = "Нічия 🤝"
        win_streak[user_id] = 0

    elif (
        (user_choice == "Камінь" and bot_choice == "Ножиці") or
        (user_choice == "Ножиці" and bot_choice == "Папір") or
        (user_choice == "Папір" and bot_choice == "Камінь")
    ):
        result = "Ти виграв 🎉"
        scores[user_id]["user"] += 1
        win_streak[user_id] += 1

    else:
        result = "Бот виграв 🤖"
        scores[user_id]["bot"] += 1
        win_streak[user_id] = 0


    bot.send_message(
        chat_id,
        f"Ти вибрав: {user_choice}\n"
        f"Бот вибрав: {bot_choice}\n\n"
        f"{result}\n\n"
        f"Рахунок:\n"
        f"Ти: {scores[user_id]['user']}\n"
        f"Бот: {scores[user_id]['bot']}\n"
        f"Win streak: {win_streak[user_id]}",
        reply_markup=game_keyboard()
    )


@bot.message_handler(func=lambda m: m.text == "⬅️ Назад")
def back(message):
    bot.send_message(
        message.chat.id,
        "Головне меню 👇",
        reply_markup=get_keyboard()
    )


@bot.message_handler(func=lambda m: m.text == "Однорукий бандит✋")
def slot_menu(message):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Крутити 🎰")
    keyboard.add("⬅️ Назад")

    bot.send_message(
        message.chat.id,
        "🎰 Однорукий бандит\nНатисни кнопку щоб крутити барабан",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda m: m.text == "Крутити 🎰")
def game2(message):

    list1 = ["🍒", "🍋", "🔔", "⭐", "💎"]

    baraban1 = random.choice(list1)
    baraban2 = random.choice(list1)
    baraban3 = random.choice(list1)

    if baraban1 == baraban2 == baraban3:
        result = "🎉 Джекпот! Ти виграв!"
    elif baraban1 == baraban2 or baraban1 == baraban3 or baraban2 == baraban3:
        result = "✨ Маленький виграш!"
    else:
        result = "💥 Спробуй ще раз!"

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Крутити 🎰")
    keyboard.add("⬅️ Назад")

    bot.send_message(
        message.chat.id,
        f"| {baraban1} | {baraban2} | {baraban3} |\n\n{result}",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda m: m.text == "Кубік рубік🎲")
def dice_game(message):
    user_roll = random.randint(1, 6)
    bot_roll = random.randint(1, 6)

    if user_roll > bot_roll:
        result = "Ти виграв! 🎉"
    elif user_roll < bot_roll:
        result = "Бот виграв! 🤖"
    else:
        result = "Нічия! 🤝"

    bot.send_message(
        message.chat.id,
        f"🎲 Ти кинув кубік і випало число: {user_roll}\n"
        f"🤖 Бот кинув кубік і випало число: {bot_roll}\n\n"
        f"{result}",
        reply_markup=get_keyboard()
    )


@bot.message_handler(func=lambda m: m.text == "Вгадай число💌")
def guess_number(message):
    number_to_guess = random.randint(1, 100)

    bot.send_message(
        message.chat.id,
        "Я загадал число від 1 до 100. Попробуй вгадати. Введи свою відповідь.",
        reply_markup=types.ReplyKeyboardRemove()
    )

    @bot.message_handler(func=lambda m: m.text.isdigit())
    def check_guess(message):
        user_guess = int(message.text)

        if user_guess < number_to_guess:
            bot.send_message(message.chat.id, "Мало")
        elif user_guess > number_to_guess:
            bot.send_message(message.chat.id, "Багато")
        else:
            bot.send_message(message.chat.id, f"Ти вгадав {number_to_guess}!")
            bot.send_message(
                message.chat.id,
                "Виберіть іншу гру або зіграйте знову 👇",
                reply_markup=get_keyboard()
            )


@bot.message_handler(func=lambda m: m.text == "💲Курс валют")
def currency_menu(message):
    bot.send_message(
        message.chat.id,
        "Выбери валюту 👇",
        reply_markup=kyrs_valut()
    )

@bot.message_handler(func=lambda m: m.text ==  "USD 💵")
def dolar(message):
    url = ("token")
    r = requests.get(url)
    data = r.json()
    for item in data:
        if item["ccy"] == "USD":
            dollar_buy = item["buy"]
            dollar_sale = item["sale"]
    text = f"💲 USD:\nПокупка: {dollar_buy}\nПродажа: {dollar_sale}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: m.text and "EUR" in m.text)
def eur(message):
    url = "token"
    r = requests.get(url)
    data = r.json()

    for item in data:
        if item["ccy"] == "EUR":
            text = f"💶 EUR:\nПокупка: {item['buy']}\nПродажа: {item['sale']}"
            bot.send_message(message.chat.id, text)
            return

@bot.message_handler(func=lambda m: m.text ==  "BTC ₿")
def btc(message):
    url = "token"
    r = requests.get(url)
    data = r.json()

    if "bitcoin" in data and "uah" in data["bitcoin"]:
        price = data["bitcoin"]["uah"]
        bot.send_message(message.chat.id, f"₿ BTC:\nЦена: {price} UAH")
    else:
        bot.send_message(message.chat.id, "Не удалось получить курс BTC")

bot.polling(none_stop=True)

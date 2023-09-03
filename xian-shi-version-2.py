import telebot
import random
import time
from telebot import types


TOKEN = 'YOUR TOKEN'
bot = telebot.TeleBot(TOKEN)

#Описание команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    tells = ['Гадание да/нет', 'Гадание по книге перемен', 'Совместимость']
    for tell in tells:
        button = types.KeyboardButton(text=tell)
        markup.add(button)
    bot.reply_to(message, 'Я -- Сйен Ши, ваш личный предсказатель.\n\nВозникли проблемы? Обратитесь к инструкции к применению командой /help\n\nДля начала гадания нажмите на кнопку с его названием ниже↓↓↓', reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, 'Команды, чтобы узнать побольше о гаданиях:\n - /book_of_changes (справка)\n - /yes_or_no (справка)\n - /zodiac_sighs (справка)\n(Справки нельзя получить во время гадания)\n\nНашли неисправность в работе? - напишите нам об этом!\nТехнический специалист - @monika_beluchiiiii', reply_markup=None)

@bot.message_handler(commands=['book_of_changes'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    markup.add('Гадание по книге перемен')
    markup.add('Вернуться назад')
    bot.reply_to(message, 'Книга Перемен — это древне-китайское гадание, чаще всего используется для получения советов.\nЧтобы погадать по Книге Перемен, выполните следующие действия:\n - выбрать её в списке гаданий\n - написать свой вопрос\n - нажать появившуюся кнопку «бросить жребий».\nВажно понимать, что в зависимости от ситуации предсказания могут трактоваться по-разному.', reply_markup=markup)

@bot.message_handler(commands=['yes_or_no'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    markup.add('Гадание да/нет')
    markup.add('Вернуться назад')
    bot.reply_to(message, 'Да/Нет — легкое гадание, которое используется для получения ответа, на который можно ответить «да» или «нет».\nЧтобы погадать с помощью него, выполните следующие действия:\n - выбрать «Да/Нет» в списке гаданий.\n - написать свой вопрос', reply_markup=markup)

@bot.message_handler(commands=['zodiac_sighs'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    markup.add('Совместимость')
    markup.add('Вернуться назад')
    bot.reply_to(message, 'Совместимость по знакам зодиака— гадание, основанное на астрологических знаках двух людей. Чтобы узнать вашу совместимость в дружбе и любви, выполните следующие действия:\n - выбрать «Совместимость» в списке гаданий\n - выбрать знак зодиака партнера (на кого гадаете)\n - выбрать свой знак зодиака', reply_markup=markup)


#Обработка запросов с главной клаиватуры
@bot.message_handler(func=lambda message: message.text == 'Вернуться назад')
def step_back(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    tells = ['Гадание да/нет', 'Гадание по книге перемен', 'Совместимость']
    for tell in tells:
        button = types.KeyboardButton(text=tell)
        markup.add(button)
    bot.reply_to(message, 'Команды, чтобы узнать побольше о гаданиях:\n - /book_of_changes\n - /yes_or_no\n - /zodiac_sighs\nДля начала гадания нажмите на кнопку с его названием ниже↓↓↓', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Гадание да/нет')
def handle_yes_no(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    markup.add('Вернуться назад')

    bot.send_message(chat_id=message.chat.id, text='Задайте ваш вопрос (воспользуйтесь обычной клавиатурой):', reply_markup=markup)

    bot.register_next_step_handler(message, answer_yes_no)

@bot.message_handler(func=lambda message: message.text == 'Гадание по книге перемен')
def handle_book_of_changes(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    markup.add('Вернуться назад')
    question = bot.reply_to(message, 'Задайте ваш вопрос (воспользуйтесь обычной клавиатурой):', reply_markup=markup)
    if message.text == 'Вернуться назад':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        tells = ['Гадание да/нет', 'Гадание по книге перемен', 'Совместимость']
        for tell in tells:
           button = types.KeyboardButton(text=tell)
           markup.add(button)
        bot.reply_to(message, 'Команды, чтобы узнать побольше о гаданиях:\n - /book_of_changes\n - /yes_or_no\n - /zodiac_sighs\nДля начала гадания нажмите на кнопку с его названием ниже↓↓↓', reply_markup=markup)
        return
    bot.register_next_step_handler(question, book_of_changes)

@bot.message_handler(func=lambda message: message.text == 'Совместимость')
def compatibility_1(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    sighs = ["Вернуться назад", "Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
    for zodiac in sighs:
        button = types.KeyboardButton(text=zodiac)
        markup.add(button)

    bot.send_message(message.chat.id, "Выберите знак зодиака, на кого гадаете", reply_markup=markup)
    bot.register_next_step_handler(message, zodiacs_1)

def zodiacs_1(message):
    global user_messages
    user_messages = {}

    if message.text == 'Вернуться назад':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        tells = ['Гадание да/нет', 'Гадание по книге перемен', 'Совместимость']
        for tell in tells:
           button = types.KeyboardButton(text=tell)
           markup.add(button)
        bot.reply_to(message, 'Команды, чтобы узнать побольше о гаданиях:\n - /book_of_changes\n - /yes_or_no\n - /zodiac_sighs\nДля начала гадания нажмите на кнопку с его названием ниже↓↓↓', reply_markup=markup)
        return
    
    bot.send_message(message.chat.id, "Выберите свой знак зодиака")
    user_messages[message.chat.id] = message.text
    bot.register_next_step_handler(message, zodiacs_2)

def zodiacs_2(message):
    if message.text == 'Вернуться назад':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        tells = ['Гадание да/нет', 'Гадание по книге перемен', 'Совместимость']
        for tell in tells:
           button = types.KeyboardButton(text=tell)
           markup.add(button)
        bot.reply_to(message, 'Команды, чтобы узнать побольше о гаданиях:\n - /book_of_changes\n - /yes_or_no\n - /zodiac_sighs\nДля начала гадания нажмите на кнопку с его названием ниже↓↓↓', reply_markup=markup)
        return
    
    previous_message_text = user_messages.get(message.chat.id)

    bot.send_message(message.chat.id, "Подбираем ответ...")
    time.sleep(1)
    bot.edit_message_text(f'{message.text} и {previous_message_text}\nСовместимость в дружбе: {random.randint(0, 100)}%\nСовместимость в любви: {random.randint(0, 100)}%\nСовместимость в бизнесе: {random.randint(0, 100)}%', message.chat.id, message.message_id + 1)

    time.sleep(1)

    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    tells = ['Гадание да/нет', 'Гадание по книге перемен', 'Совместимость']
    for tell in tells:
        button = types.KeyboardButton(text=tell)
        markup.add(button)
    bot.send_message(message.chat.id, 'Для начала нового гадания выберите его тип↓↓↓', reply_markup=markup)
    
    
#Механизмы гаданий
def answer_yes_no(message):
    if message.text == 'Вернуться назад':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        tells = ['Гадание да/нет', 'Гадание по книге перемен', 'Совместимость']
        for tell in tells:
           button = types.KeyboardButton(text=tell)
           markup.add(button)
        bot.reply_to(message, 'Команды, чтобы узнать побольше о гаданиях:\n - /book_of_changes\n - /yes_or_no\n - /zodiac_sighs\nДля начала гадания нажмите на кнопку с его названием ниже↓↓↓', reply_markup=markup)
        return
    
    answer = random.choice(['Да', 'Нет', 'Все зависит от вас'])
    
    bot.send_message(message.chat.id, "Подбираем ответ...")

    # Запускаем функцию с изменением ответа через 1 секунду
    time.sleep(1)
    bot.edit_message_text(answer, message.chat.id, message.message_id + 1)
    
    time.sleep(1)
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    tells = ['Гадание да/нет', 'Гадание по книге перемен', 'Совместимость']
    for tell in tells:
        button = types.KeyboardButton(text=tell)
        markup.add(button)
    bot.send_message(message.chat.id, 'Для начала нового гадания выберите его тип↓↓↓', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Гадание по книге перемен')
def book_of_changes(message):
    if message.text == 'Вернуться назад':
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        tells = ['Гадание да/нет', 'Гадание по книге перемен', 'Совместимость']
        for tell in tells:
           button = types.KeyboardButton(text=tell)
           markup.add(button)
        bot.reply_to(message, 'Команды, чтобы узнать побольше о гаданиях:\n - /book_of_changes\n - /yes_or_no\n - /zodiac_sighs\nДля начала гадания нажмите на кнопку с его названием ниже↓↓↓', reply_markup=markup)
        return
    
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Бросить жребий", callback_data="throw_coin")
    markup.add(button)

    bot.send_message(message.chat.id, "Для получения ответа брось жребий", reply_markup=markup)


#Обработка inline команд
@bot.callback_query_handler(func=lambda call: True)
def inline_keyboard_handler(call):
    #Механизм гадания по Книге Перемен
    if call.data == "throw_coin":

        bot.send_message(call.message.chat.id, "Генерация номера гексаграммы:")

        # Запускаем функцию с изменением ответа через 1 секунду
        time.sleep(1)

        gex = ''
        gex_elements = ['!', '|']

        for i in range(4):
            random_ch = random.randint(0, 1)
            time.sleep(0.3)
            gex += gex_elements[random_ch]
            bot.edit_message_text(f'Генерация номера гексаграммы: {gex}', call.message.chat.id, call.message.message_id + 1)

        number = int(''.join(['0' if i == '!' else '1' for i in gex]), 2)

        image_path = f'image{number + 1}.jpeg'
        
        with open(f"/Users/catalina/Documents/гадалка/{image_path}", 'rb') as photo:
            time.sleep(1)
            bot.send_photo(call.message.chat.id, photo)

        with open('predicts.txt', 'rb') as file:
            text = file.read().decode('utf-8')
            predict = text.split('\n')[number]

        bot.send_message(call.message.chat.id, f'Номер гексаграмы: {number + 1}\n{predict}')
        time.sleep(1)
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        tells = ['Гадание да/нет', 'Гадание по книге перемен', 'Совместимость']
        for tell in tells:
            button = types.KeyboardButton(text=tell)
            markup.add(button)
        bot.send_message(call.message.chat.id, 'Для начала нового гадания выберите его тип↓↓↓', reply_markup=markup)
    
bot.polling()

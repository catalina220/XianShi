import telebot
import random
import time
from telebot import types


TOKEN = '6670214969:AAGf4O3ZdNPSMbzWsf3e_txgywTPGBKUAsY'
bot = telebot.TeleBot(TOKEN)

#Клавиатура выбора гаданий
keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3)
keyboard.add(telebot.types.KeyboardButton('Гадание да/нет'), telebot.types.KeyboardButton('Гадание по книге перемен'), telebot.types.KeyboardButton('Совместимость'))


#Описание команд
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я бот-гадалка. Чем я могу помочь? Команды, чтобы узнать побольше о гаданиях:\n - /book_of_changes\n - /yes_or_no\n - /zodiac_sighs', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, 'Тут должна быть помощь пользователям.', reply_markup=keyboard)

@bot.message_handler(commands=['book_of_changes'])
def send_welcome(message):
    bot.reply_to(message, 'Книга Перемен — это древне-китайское гадание, чаще всего используется для получения советов.\nЧтобы погадать по Книге Перемен, выполните следующие действия:\n - выбрать её в списке гаданий\n - написать свой вопрос\n - нажать появившуюся кнопку «бросить жребий».\nВажно понимать, что в зависимости от ситуации предсказания могут трактоваться по-разному.', reply_markup=keyboard)

@bot.message_handler(commands=['yes_or_no'])
def send_welcome(message):
    bot.reply_to(message, 'Да/Нет — легкое гадание, которое используется для получения ответа, на который можно ответить «да» или «нет».\nЧтобы погадать с помощью него, выполните следующие действия:\n - выбрать «Да/Нет» в списке гаданий.\n - написать свой вопрос', reply_markup=keyboard)

@bot.message_handler(commands=['zodiac_sighs'])
def send_welcome(message):
    bot.reply_to(message, 'Совместимость — гадание, основанное на астрологических знаках двух людей. Чтобы узнать вашу совместимость в дружбе и любви, выполните следующие действия:\n - выбрать «Совместимость» в списке гаданий\n - выбрать знак зодиака партнера (на кого гадаете)\n - выбрать свой знак зодиака', reply_markup=keyboard)


#Обработка запросов с главной клаиватуры
@bot.message_handler(func=lambda message: message.text == 'Гадание да/нет')
def handle_yes_no(message):
    question = bot.reply_to(message, 'Задайте ваш вопрос:')
    bot.register_next_step_handler(question, answer_yes_no)

@bot.message_handler(func=lambda message: message.text == 'Гадание по книге перемен')
def handle_book_of_changes(message):
    question = bot.reply_to(message, 'Задайте ваш вопрос:')
    bot.register_next_step_handler(question, book_of_changes)

@bot.message_handler(func=lambda message: message.text == 'Совместимость')
def compatibility_1(message):
    markup = types.InlineKeyboardMarkup()

    sighs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
    for zodiac in sighs:
        button = types.InlineKeyboardButton(text=zodiac, callback_data="to_know_comp")
        markup.add(button)

    bot.send_message(message.chat.id, "Выберите знак зодиака, на кого гадаете", reply_markup=markup)


#Механизмы гаданий
def answer_yes_no(message):
    answer = random.choice(['Да', 'Нет'])
    time.sleep(2)
    bot.reply_to(message, answer)
    bot.send_message(message.chat.id, 'Хотите еще гадание?', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Гадание по книге перемен')
def book_of_changes(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Бросить жребий", callback_data="throw_coin")
    markup.add(button)

    bot.send_message(message.chat.id, "Для получения ответа брось жребий", reply_markup=markup)


#Обработка inline команд
@bot.callback_query_handler(func=lambda call: True)
def inline_keyboard_handler(call):

    #Механизм гадания по Книге Перемен
    if call.data == "throw_coin":
        number = random.randint(0, 26)

        #Список, где будут храниться значения гексограмм. При значительном увеличении количества значений можно перевести в отдельнй json файл.
        
        images = ['image1.jpeg', 'image2.jpeg', 'image3.jpeg', 'image4.jpeg', 'image5.jpeg', 'image6.jpeg', 'image7.jpeg', 'image8.jpeg', 'image9.jpeg', 'image10.jpeg', 'image11.jpeg', 'image12.jpeg', 'image13.jpeg', 'image14.jpeg', 'image15.jpeg', 'image16.jpeg', 'image17.jpeg', 'image18.jpeg', 'image19.jpeg', 'image20.jpeg', 'image21.jpeg', 'image22.jpeg', 'image23.jpeg', 'image24.jpeg', 'image25.jpeg', 'image26.jpeg', 'image27.jpeg']
        image_path = images[number]

        with open(f"/Users/catalina/Documents/гадалка/{image_path}", 'rb') as photo:
            time.sleep(2)
            bot.send_photo(call.message.chat.id, photo)

        predicts = ['Чиен (Творчество) - Силу своего разума направь на достижение великих целей.',
                    'Хун (Покорность) - Познай свое место и прими свою участь.',
                    'Чжун Чжэнь (Начальная трудность) - Будь терпеливым и уверенным в достижении цели.',
                    'Мэнь (Соприкосновение) - Устанавливай гармоничные отношения с другими.',
                    'Су (Ожидание) - Будь терпеливым и доверься ходу событий.',
                    'Сунь (Поддержка) - Ищи поддержку внутри и вовне.',
                    'Ши хо (Урожайный отряд) - Работай в команде и достигай успеха вместе.',
                    'Би (Сокрушение) - Переживи кризис и выйди из него сильнее.',
                    'Бо (Разобщение) - Будь терпеливым и доверься процессу изменения.',
                    'Фу (Возврат) - Верни себя и восстанови гармонию в своей жизни.',
                    'У (Невинность) - Следуй своим истинным убеждениям и будь искренним.',
                    'Да чу (Соединение тающего) - Объединяй различные аспекты своей жизни в единое целое.',
                    'И (Продолжение) - Будь выносливым и продолжай двигаться вперед.',
                    'Да го (Прекрепление) - Поддерживай прочность и устойчивость в своей жизни.',
                    'Кань (Судьба) - Прими свою судьбу и работай с ней для достижения своей цели.',
                    'Ли (Сияние) - Используй свою силу и внутренний свет для освещения других.',
                    'Цижиань (Преграда) - Ищи способы преодолевать преграды на своем пути.',
                    'Хиэ (Объединение) - Объединяйся с другими и работай вместе для достижения общей цели.',
                    'Сунь (Убыль) - Убери все ненужное из своей жизни и освободись.',
                    'Шень (Подъем) - Поднимайся над ситуацией и преодолевай трудности.',
                    'Кунь (Истощение) - Отдавай и распространяй свою энергию мудро и с умом.',
                    'Цзинь (Истощение) - Найди баланс и береги свою энергию и ресурсы.',
                    'Гэ (Разминирование) - Разреши старые проблемы и конфликты, чтобы двигаться вперед.'                    
                    'Дзин (Котел) - Претерпевай изменения и процессы трансформации.',
                    'Цень (Перевоплощение) - Приспосабливайся к переменам и переосмысливай свою жизнь.',
                    'Кань (Тишина) - Найди моменты покоя и умиротворения в своей жизни.',
                    'Джянь (Прогресс) - Достижение успеха через инновации и прогресс.',
                    'Шень (Подъем) - Поднимайся над ситуацией и преодолевай трудности.']

        bot.send_message(call.message.chat.id, f'Номер гексограмы: {number}\n{predicts[number]}')    
        bot.send_message(call.message.chat.id, 'Хотите еще гадание?', reply_markup=keyboard)
        
    #Механизм гадания на совместимость
    if call.data == "to_know_comp":
        markup = types.InlineKeyboardMarkup() 
        
        sighs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
        for zodiac in sighs:
            button = types.InlineKeyboardButton(text=zodiac, callback_data="to_know_comp_answer")
            markup.add(button)

        bot.send_message(call.message.chat.id, "Выберите свой знак зодиака", reply_markup=markup)

    if call.data == "to_know_comp_answer":
        time.sleep(2)
        bot.send_message(call.message.chat.id, f"Совместимость в любви: {random.randint(0, 101)}%\nСовместимость в дружбе: {random.randint(0, 101)}%")
        bot.send_message(call.message.chat.id, 'Хотите еще гадание?', reply_markup=keyboard)


bot.polling()
import telebot
from telebot import types


class Place:

    def __init__(self, place_name):
        self.photo_list = []
        self.place_name = place_name
        self.description = None

    def add_photo(self, photo):
        if photo:
            self.photo_list.append(photo)
        return len(self.photo_list)

    def add_description(self, user_description):
        self.description = user_description
        return bool(self.description)


class TelegramBot:
    start_button = {}
    user_list = {}
    places = []
    name_place = None

    def __init__(self, token):
        self.token = token
        self.bot = telebot.TeleBot(self.token)
        self.markup_inline = types.InlineKeyboardMarkup()
        self.markup_reply = None

    def get_chat_id_and_start(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            if message.from_user.id not in self.user_list:
                self.user_list.setdefault(message.from_user.id, [])
            if message.chat.id not in self.start_button:
                self.markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton('Добавить фото')
                btn2 = types.KeyboardButton('Посмотреть фото')
                self.markup_reply.row(btn2, btn1)

                self.start_button[message.chat.id] = self.markup_reply

                self.bot.send_message(message.chat.id, 'Привет', reply_markup=self.markup_reply)
            else:
                self.bot.send_message(message.chat.id, "Привет!",
                                      reply_markup=self.start_button[message.chat.id])

    @staticmethod
    def check_place(user_list: list, text):
        for item in user_list:
            if item.place_name == text:
                return user_list[user_list.index(item)]
        return False

    def button_click_add_photo(self):

        @self.bot.message_handler(func=lambda message: message.text == 'Посмотреть фото')
        def look_photo(mess):
            markup = types.InlineKeyboardMarkup()

            for place in self.user_list[mess.from_user.id]:
                markup.add(types.InlineKeyboardButton(text=place.place_name, callback_data=place.place_name))
            self.bot.send_message(mess.chat.id, 'Выбери место', reply_markup=markup)

            @self.bot.callback_query_handler(func=lambda callback: True)
            def callback_func(callback):
                for place_from_callback in self.user_list[mess.from_user.id]:
                    place_name = place_from_callback.place_name
                    if callback.data == place_name:
                        self.bot.send_message(mess.chat.id, place_name)
                        for pic in place_from_callback.photo_list:
                            self.bot.send_photo(mess.chat.id, photo=pic)
                        break
                    else:
                        continue

        @self.bot.message_handler(func=lambda message: message.text == 'Добавить фото')
        def app_photo(message):
            markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_start = types.KeyboardButton('/start')
            markup_start.row(btn_start)
            self.bot.send_message(message.chat.id, 'Введи место', reply_markup=markup_start)

            @self.bot.message_handler(content_types=['text'])
            def get_name_place(mess_name_place):
                if not self.check_place(self.user_list[mess_name_place.from_user.id], mess_name_place.text):
                    self.user_list[mess_name_place.from_user.id].append(Place(mess_name_place.text))
                    self.name_place = mess_name_place.text
                else:
                    self.name_place = mess_name_place.text
                self.bot.send_message(mess_name_place.chat.id, 'Добавь фотографию')

                @self.bot.message_handler(content_types=['photo'])
                def get_photo(message_for_photo):
                    photo_id = message_for_photo.photo[-1].file_id
                    place = self.check_place(self.user_list[message_for_photo.from_user.id], self.name_place)
                    place.add_photo(photo_id)
                    self.bot.send_message(message_for_photo.chat.id, "Вы в главном меню!",
                                          reply_markup=self.start_button[message.chat.id])

    def pull(self):
        self.get_chat_id_and_start()
        self.button_click_add_photo()
        self.bot.polling(none_stop=True)


token_bot = "5548068409:AAFHj4UkbPkyUh5QlZ5la3CJqGnECNWpI1g"

bot = TelegramBot(token_bot)
bot.pull()

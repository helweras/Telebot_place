import telebot
from telebot import types


class Place:
    pass


class TelegramBot:
    start_button = {}
    user_photo = {}
    places = []

    def __init__(self, token):
        name_place = None
        self.token = token
        self.bot = telebot.TeleBot(self.token)
        self.markup_inline = types.InlineKeyboardMarkup()
        self.markup_reply = None
        self.chat_id = None
        self.user_id = None

    def get_chat_id_and_start(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.chat_id = message.chat.id
            self.user_id = message.from_user.id
            if not self.start_button:
                self.markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton('Добавить фото')
                btn2 = types.KeyboardButton('Посмотреть фото')
                self.markup_reply.row(btn2, btn1)

                self.start_button[self.chat_id] = self.markup_reply

                self.bot.send_message(self.chat_id, 'Привет', reply_markup=self.markup_reply)
            else:
                self.bot.send_message(self.chat_id, "Привет!",
                                      reply_markup=self.start_button[self.chat_id])

    def button_click_add_photo(self):

        @self.bot.message_handler(func=lambda message: message.text == 'Посмотреть фото')
        def look_photo(mess):
            for pic_list in self.user_photo[self.user_id]:
                for pic in self.user_photo[self.user_id][pic_list]:
                    self.bot.send_photo(self.chat_id, photo=pic)

        @self.bot.message_handler(func=lambda message: message.text == 'Добавить фото')
        def app_photo(message):
            markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_start = types.KeyboardButton('/start')
            markup_start.row(btn_start)
            self.bot.send_message(self.chat_id, 'Введи место', reply_markup=markup_start)

            @self.bot.message_handler(content_types=['text'])
            def get_name_place(mess):
                self.name_place = mess.text
                tmp_dict = {self.name_place: []}
                if self.user_id not in self.user_photo:
                    self.user_photo[self.user_id] = tmp_dict
                    self.bot.send_message(self.chat_id, 'Добавь фотографию')
                else:
                    self.user_photo[self.user_id][self.name_place] = []
                    self.bot.send_message(self.chat_id, 'Добавь фотографию')

                @self.bot.message_handler(content_types=['photo'])
                def get_photo(message_for_photo):
                    print(message_for_photo.media_group_id)
                    photo_id = message_for_photo.photo[-1].file_id
                    self.user_photo[self.user_id][self.name_place].append(photo_id)
                    self.bot.send_message(self.chat_id, "Вы в главном меню!",
                                          reply_markup=self.start_button[self.chat_id])

    def pull(self):
        self.get_chat_id_and_start()
        self.button_click_add_photo()
        self.bot.polling(none_stop=True)


token = "5548068409:AAFHj4UkbPkyUh5QlZ5la3CJqGnECNWpI1g"

bot = TelegramBot(token)
bot.pull()

import telebot
from telebot import types
import requests
from random import choice
import json


class Place:

    def __init__(self, place_name):
        self.photo_list = []
        self.place_name = place_name
        self.description = None

    def add_photo(self, photo=False):
        if photo:
            self.photo_list.append(photo)
        else:
            return len(self.photo_list)

    def add_description(self, user_description):
        self.description = user_description
        return bool(self.description)

    def data_for_write(self):
        return {'place_name': self.place_name, 'description': self.description, 'photo_list': self.photo_list}


class TelegramBot:
    funny_answer = ("На этой фотке явно чувствуется искусство... или просто случайное нажатие кнопки?",
                    "Если бы это была искусственная разведка, это была бы фотка, которую они отправили бы случайно и сказали: 'Ой, неправильный файл!'",
                    "Фото, которое кричит: 'Пора протереть объектив!' Но, может быть, пыль – это новый тренд?",
                    "Интересно, что хотел сказать фотограф этой картиной. Видимо, что-то очень глубокое, потому что я не понял.",
                    "На этой фотке как будто кто-то пытается заставить нас поверить, что пятно на стене – это искусство. Ждем следующее 'пятно-шедевр'!",
                    "Эта фотография словно говорит: 'Я не знаю, что является объектом съемки, но я уверен, что это должно быть круто!'",
                    "Интересный выбор ракурса. Возможно, фотограф решил показать нам мир глазами пылинок на линзе.",
                    "Как будто кто-то случайно выставил экспозицию на 10 минут и случайно нажал кнопку. Но, по крайней мере, получилась интересная абстракция!",
                    "Фото, которое явно имеет свою историю. Возможно, она заключается в том, что фотограф забыл, что камера включена.",
                    "Кажется, кто-то случайно нажал на кнопку 'Сделать фото' во время падения камеры. Удивительно, что что-то вообще получилось!",
                    "Эта фотография как будто говорит: 'Я хотела бы что-то сказать, но не знаю, что'.",
                    "Фото, которое делалось так долго, что объект съемки успел вырасти.",
                    "Кажется, фотограф решил подчеркнуть красоту хаоса на этой картине.",
                    "На этой фотке можно увидеть, как идеи разлетаются на все стороны, как конфетти на празднике.",
                    "Как будто кто-то попытался запечатлеть душу предмета. Жаль, что у предмета ее нет.",
                    "Эта фотография словно кричит: 'Я искусство!' Нам только нужно понять, что именно.",
                    "Кажется, фотограф смешал все свои идеи в одну кастрюлю и это – результат.",
                    "На этой фотографии как будто запечатлен момент, когда солнце решило покинуть рамки обыденности и стало сиять ярче.",
                    "Фотография, которая намекает: 'Возможно, что-то важное происходит за пределами кадра. Но что – тайна'.",
                    "Как будто кто-то случайно уронил камеру и случайно сделал этот кадр. Удачное случайное произведение искусства!",
                    "На этой фотке, как будто кто-то решил изучить понятие 'абстракция', не заботясь о зрителях.",
                    "Кажется, фотограф смотрел на мир через призму хаоса и случайности – и вот результат.",
                    "Эта фотография, как будто говорит: 'Является ли кто-то кем-то? Мир – иллюзия'.",
                    "На этой фотке можно увидеть, как случайность становится искусством – или наоборот.",
                    "Как будто кто-то пытался зафиксировать момент творческого взрыва идей. Жаль, что это больше похоже на взрыв конфети.",
                    "Эта фотография словно кричит: 'Фотография – это не о предмете, а о чувствах'. А мы так и не поняли, о каких именно чувствах идет речь.",
                    "Кажется, фотограф сделал эту картину, закрыв глаза и случайно нажимая на кнопки камеры. Удивительно, что что-то в итоге получилось.",
                    "На этой фотографии как будто кто-то пытался поймать душу объекта, но что-то пошло не так. Видимо, объект был слишком быстр.",
                    "Фотография, которая говорит: 'Предмет – это просто иллюзия, и мы – жертвы этой иллюзии'. Впечатляюще философский кадр.",
                    "Как будто кто-то случайно поднес камеру к чему-то интересному и случайно нажал на кнопку. Может быть, именно так рождаются шедевры!"
                    )
    start_button = {}
    user_list = {}
    name_place = {}

    def __init__(self, token):
        self.token = token
        self.bot = telebot.TeleBot(self.token)
        self.markup_inline = types.InlineKeyboardMarkup()
        self.markup_reply = None

    @staticmethod
    def interpreter_for_record(user_list: dict, key):
        """Возвращает словарь для записи в формат json в виде:
        {user_id: [{'place_name': 'name:str', 'description': str, 'photo_list': ['photo_id':str]}]}
        """
        data_for_record = dict()
        data_for_record[key] = []
        for item in user_list[key]:
            if isinstance(item, Place):
                data_for_record[key].append(item.data_for_write())
        return data_for_record

    @staticmethod
    def record_data(data: dict):
        file_name = 'data_users.json'
        key = list(data.keys())[-1]
        try:
            with open(file_name, 'r', encoding='utf-8') as file_read:
                old = json.load(file_read)
        except FileNotFoundError:
            old = {}
        with open(file_name, 'w', encoding='utf-8') as file_record:
            if old:
                if str(key) in old:
                    for place in data[key]:
                        if place not in old[str(key)]:
                            old[str(key)].append(place)
                else:
                    old.setdefault(key, data)
                json.dump(old, file_record)

            else:
                json.dump(data, file_record)

    @staticmethod
    def read_data(key, file_name='data_users.json'):
        with open(file_name, encoding='utf-8') as file_read:
            tmp_user_list = json.load(file_read)
            return tmp_user_list[key]

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
            if self.user_list:
                for place in self.user_list[mess.from_user.id]:
                    markup.add(types.InlineKeyboardButton(text=place.place_name, callback_data=place.place_name))
            else:
                for place in self.read_data(mess.from_user.id):
                    markup.add(types.InlineKeyboardButton(text=place['place_name'], callback_data=place['place_name']))
            self.bot.send_message(mess.chat.id, 'Выбери место', reply_markup=markup)

            @self.bot.callback_query_handler(func=lambda callback: True)
            def callback_func(callback):
                for place_from_callback in self.user_list[mess.from_user.id]:
                    place_name = place_from_callback.place_name
                    if callback.data == place_name:
                        media_group = []
                        self.bot.send_message(mess.chat.id, place_name)
                        for pic in place_from_callback.photo_list:
                            file_info = self.bot.get_file(pic)
                            file_url = f"https://api.telegram.org/file/bot{self.token}/{file_info.file_path}"
                            response = requests.get(file_url)
                            media_group.append(types.InputMediaPhoto(media=response.content))
                        self.bot.send_media_group(mess.chat.id, media_group)
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
                    self.name_place[mess_name_place.chat.id] = mess_name_place.text
                else:
                    self.name_place[mess_name_place.chat.id] = mess_name_place.text
                self.bot.send_message(mess_name_place.chat.id, 'Добавь фотографию')

                @self.bot.message_handler(content_types=['photo'])
                def get_photo(message_for_photo):
                    photo_id = message_for_photo.photo[-1].file_id
                    place = self.check_place(self.user_list[message_for_photo.from_user.id],
                                             self.name_place[mess_name_place.chat.id])
                    place.add_photo(photo_id)
                    self.bot.reply_to(message_for_photo,
                                      choice(self.funny_answer),
                                      reply_markup=self.start_button[message.chat.id])

                    data_for_record = self.interpreter_for_record(self.user_list, mess_name_place.chat.id)
                    print(data_for_record)
                    self.record_data(data_for_record)

    def pull(self):
        self.get_chat_id_and_start()
        self.button_click_add_photo()
        self.bot.polling(none_stop=True)


token_bot = "5548068409:AAFHj4UkbPkyUh5QlZ5la3CJqGnECNWpI1g"

bot = TelegramBot(token_bot)
bot.pull()

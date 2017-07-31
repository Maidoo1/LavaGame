'''
'The floor is lava' game for Telegram

Maidoo
31.07.17
'''

import telebot

tb_token = '407083820:AAFB66RmIckJ1H46Uz_rmvR55pbVRPy5f_I'

bot = telebot.TeleBot(tb_token)


class LavaGame:
    dict = {}

    def __init__(self, room_num):
        self.room_num = room_num
        self.started = False
        self.max_time = 30

    def set_time(self, max_time):
        self.max_time = max_time

    def start(self, id):
        self.started = True
        bot.send_message(id, 'Игра началась!')

room_dict = {}


def isHost(id, room=room_dict):
    if str(id) in room_dict.keys():
        return True
    else:
        return False


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.send_message(message.chat.id,\
                     'Привет, для создания комнаты введи /host, для присоединения к комнате введи /join')


@bot.message_handler(commands=['host'])
def handle_start(message):
    room_num = str(message.text).split()[-1]
    room_dict[str(message.chat.id)] = LavaGame(room_num)
    bot.send_message(message.chat.id,\
                     'Вы создали комнату с id {}'.format(room_num))
    print(room_dict)


@bot.message_handler(commands=['join'])
def handle_start(message):
    bot.send_message(message.chat.id,\
                     'Команда для присоединения к комнате')


@bot.message_handler(commands=['time'])
def handle_start(message):
    max_time = str(message.text).split()[-1]
    if isHost(message.chat.id):
        bot.send_message(message.chat.id,\
                         LavaGame.set_time(max_time))
    else:
        bot.send_message(message.chat.id,\
                         'Только создатель комнаты имеет право устанавливать время')


@bot.message_handler(commands=['play'])
def handle_start(message):
    LavaGame.start(LavaGame, message.chat.id)

if __name__ == '__main__':
    bot.polling(none_stop=True)
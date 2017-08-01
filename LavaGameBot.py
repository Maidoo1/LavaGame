import telebot
import threading
from random import randint

tb_token = '407083820:AAFB66RmIckJ1H46Uz_rmvR55pbVRPy5f_I'

bot = telebot.TeleBot(tb_token)


class LavaGame:
    def __init__(self, host_id, channel_id):
        self.host_id = host_id
        self.channel_id = channel_id
        self.started = False
        self.safe_time = 3
        self.max_time = 30
        self._lava_timer = 0
        self._wave_timer = 0
        self._random_num = 0

    def set_time(self, max_time):
        self.max_time = max_time

    def set_safe_time(self, safe_time):
        self.safe_time = safe_time

    def lava_coming(self):
        bot.send_message(self.host_id, 'Hide! Lava is coming after:')
        for sec in range(self.safe_time, 0, -1):
            self._lava_timer = threading.Timer(1, bot.send_message(self.host_id, str(sec)))
            self._lava_timer.start()
            self._lava_timer.join()
        else:
            bot.send_message(self.host_id, 'The floor is lava!')

    def wave_timer(self):
        for sec in range(self.max_time, 0, -1):
            self._random_num = randint(0, sec)
            if self._random_num == sec:
                return self.lava_coming()
            else:
                self._wave_timer = threading.Timer(1, bot.send_message(self.host_id, 'Waiting for lava . . .'))
                self._wave_timer.start()
                self._wave_timer.join()
        else:
            return self.lava_coming()
    # def start(self, id):
    #     self.started = True
    #     bot.send_message(id, 'Игра началась!')
    #
    #     for sec in range(1, self.max_time):
    #         rand = randint(1, self.max_time)
    #         if rand == sec:
    #             return lava_coming(id)

channels_dict = {} # Словарь, в котором ключ - id хоста, а значение - объект канала


def isHost(id, room=channels_dict):
    return True if str(id) in channels_dict.keys() else False


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.send_message(message.chat.id,\
                     'Привет, для создания комнаты введи /host, для присоединения к комнате введи /join')


@bot.message_handler(commands=['host'])
def handle_start(message):
    channel_id = str(message.text).split()[-1]
    channels_dict[str(message.chat.id)] = LavaGame(message.chat.id, channel_id)
    bot.send_message(message.chat.id,\
                     'Вы создали комнату с id {}'.format(channel_id))
    print(channels_dict)


# @bot.message_handler(commands=['join'])
# def handle_start(message):
#     bot.send_message(message.chat.id,\
#                      'Команда для присоединения к комнате')


@bot.message_handler(commands=['time'])
def handle_start(message):
    max_time = str(message.text).split()[-1]
    if isHost(message.chat.id):
        bot.send_message(message.chat.id, channels_dict[str(message.chat.id)].set_time(int(max_time)))
    else:
        bot.send_message(message.chat.id,\
                         'Только создатель комнаты имеет право устанавливать время!')


@bot.message_handler(commands=['play'])
def handle_start(message):
    if isHost(message.chat.id):
        channels_dict[str(message.chat.id)].wave_timer()
    else:
        bot.send_message(message.chat.id,\
                         'Только создатель комнаты имеет право начинать игру!')


if __name__ == '__main__':
    bot.polling(none_stop=True)
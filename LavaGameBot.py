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
        self.repeat = 1
        self.safe_time = 3
        self.max_time = 30
        self._lava_timer = 0
        self._wave_timer = 0
        self._random_num = 0

    def start_game(self):
        for i in range(self.repeat):
            self.wave_timer()

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




games = {} # Словарь, в котором ключ - id хоста, а значение - объект канала


def isHost(id, room=games):
    return True if str(id) in games.keys() else False


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.send_message(message.chat.id,\
                     'Привет, для создания комнаты введи /host, для присоединения к комнате введи /join')


@bot.message_handler(commands=['host'])
def handle_start(message):
    channel_id = str(message.text).split()[-1]
    games[str(message.chat.id)] = LavaGame(message.chat.id, channel_id)
    bot.send_message(message.chat.id,\
                     'Game has been created with id: {}'.format(channel_id))
    print(games)


# @bot.message_handler(commands=['join'])
# def handle_start(message):
#     bot.send_message(message.chat.id,\
#                      'Команда для присоединения к комнате')


@bot.message_handler(commands=['time'])
def handle_start(message):
    max_time = str(message.text).split()[-1]
    if isHost(message.chat.id):
        games[str(message.chat.id)].max_time = int(max_time)
        bot.send_message(message.chat.id, 'Maximum wave time is {} now'.format(max_time))
    else:
        bot.send_message(message.chat.id,\
                         'Only host can set time!')


@bot.message_handler(commands=['safe'])
def handle_start(message):
    safe_time = str(message.text).split()[-1]
    if isHost(message.chat.id):
        games[str(message.chat.id)].safe_time = int(safe_time)
        bot.send_message(message.chat.id, 'Safe time is {} now'.format(safe_time))
    else:
        bot.send_message(message.chat.id,\
                         'Only host can set safe time!')


@bot.message_handler(commands=['repeat'])
def handle_start(message):
    iter = str(message.text).split()[-1]
    if isHost(message.chat.id):
        games[str(message.chat.id)].repeat = int(iter)
        bot.send_message(message.chat.id, 'Game will be repeated {} times'.format(iter))
    else:
        bot.send_message(message.chat.id, 'Only host can stop the game!')


@bot.message_handler(commands=['play'])
def handle_start(message):
    if isHost(message.chat.id):
        games[str(message.chat.id)].start_game()
    else:
        bot.send_message(message.chat.id,\
                         'Only host can start the game!')


if __name__ == '__main__':
    bot.polling(none_stop=True)
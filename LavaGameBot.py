import telebot
import threading
from random import randint

tb_token = '407083820:AAFB66RmIckJ1H46Uz_rmvR55pbVRPy5f_I'

bot = telebot.TeleBot(tb_token)


class LavaGame:
    def __init__(self, player_id, channel_id):
        self.players = []
        self.player_id = player_id
        self.channel_id = channel_id
        self.repeat = 1
        self.safe_time = 3
        self.max_time = 30
        self._lava_timer = 0
        self._wave_timer = 0
        self._random_num = 0

    def add_player(self, player_id):
        # self.players.update({0: player_id})
        # self.players[0] = self.player_id
        self.players.append(player_id)
        print(self.players)
        print(type(self))

    def send_messages(self, message):
        # for player in list(self.players.values()):
        #     bot.send_message(player, message)
        [bot.send_message(player, message) for player in self.players]

    def start_game(self):
        print(self.players)
        for i in range(self.repeat):
            self.wave_timer()

    def lava_coming(self):
        self.send_messages('Hide! Lava is coming after:')

        for sec in range(self.safe_time, 0, -1):
            self._lava_timer = threading.Timer(1, self.send_messages(str(sec)))
            self._lava_timer.start()
            self._lava_timer.join()

        self.send_messages('The floor is lava!')

        for sec in range(1, 4, 1):
            self._lava_timer = threading.Timer(1, lambda x: x)
            self._lava_timer.start()
            self._lava_timer.join()

        self.send_messages('The floor is safe now')

    def wave_timer(self):
        for sec in range(self.max_time, 0, -1):
            self._random_num = randint(0, sec)
            if self._random_num == sec:
                return self.lava_coming()
            else:
                self._wave_timer = threading.Timer(1, self.send_messages('Waiting for lava . . .'))
                self._wave_timer.start()
                self._wave_timer.join()
        else:
            return self.lava_coming()


games = {}  # Словарь, в котором ключ - id хоста, а значение - объект канала


def is_host(player_id, room=games):
    return True if str(player_id) in games.keys() else False


def host_id(games, channel_id):
    for host_id, game in games.items():
        if game.channel_id == channel_id:
            return host_id


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,\
                     'Hi! I`m \'The floor is lava\' game. Let`s play!\n'
                     '/host - create room\n'
                     '/join - join room\n'
                     '/play - start the game!\n'
                     '/help - if you want to change game options, call help!\n'
                     'Remember, only host of the room can change the game options and start the game!\n')


@bot.message_handler(commands=['help'])
def handle_start(message):
    bot.send_message(message.chat.id,\
                     '/time - maximum time of waves (standard - 30)\n'
                     '/safe - safe time before lava is coming (standard - 3)\n'
                     '/repeat - repeats of coming lava waves (standard - 1)\n')


@bot.message_handler(commands=['host'])
def handle_start(message):
    channel_id = str(message.text).split()[-1]
    games[str(message.chat.id)] = LavaGame(message.chat.id, channel_id)
    games[str(message.chat.id)].add_player(message.chat.id)
    print(games[str(message.chat.id)])
    bot.send_message(message.chat.id, 'Game has been created with id: {}'.format(channel_id))


@bot.message_handler(commands=['join'])
def handle_start(message):
    channel_id = str(message.text).split()[-1]
    games[host_id(games, channel_id)].player_id = message.chat.id
    games[host_id(games, channel_id)].add_player(message.chat.id)
    print(games[host_id(games, channel_id)])
    bot.send_message(message.chat.id, 'You have been joined in room: {}'.format(channel_id))


@bot.message_handler(commands=['time'])
def handle_start(message):
    max_time = str(message.text).split()[-1]
    if is_host(message.chat.id):
        games[str(message.chat.id)].max_time = int(max_time)
        bot.send_message(message.chat.id, 'Maximum wave time is {} now'.format(max_time))
    else:
        bot.send_message(message.chat.id, 'Only host can set time!')


@bot.message_handler(commands=['safe'])
def handle_start(message):
    safe_time = str(message.text).split()[-1]
    if is_host(message.chat.id):
        games[str(message.chat.id)].safe_time = int(safe_time)
        bot.send_message(message.chat.id, 'Safe time is {} now'.format(safe_time))
    else:
        bot.send_message(message.chat.id, 'Only host can set safe time!')


@bot.message_handler(commands=['repeat'])
def handle_start(message):
    iter = str(message.text).split()[-1]
    if is_host(message.chat.id):
        games[str(message.chat.id)].repeat = int(iter)
        bot.send_message(message.chat.id, 'Game will be repeated {} times'.format(iter))
    else:
        bot.send_message(message.chat.id, 'Only host can stop the game!')



@bot.message_handler(commands=['play'])
def handle_start(message):
    if is_host(message.chat.id):
        games[str(message.chat.id)].start_game()
    else:
        bot.send_message(message.chat.id, 'Only host can start the game!')


if __name__ == '__main__':
    bot.polling(none_stop=True)
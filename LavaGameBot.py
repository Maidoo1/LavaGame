import telebot
import threading
from random import randint

fire = u'\U0001F525'
hourglass = u'\U0000231B'
watch = u'\U0000231A'
recycling = u'\U0000267B'
smile = u'\U0001F47B'
point = u'\U0000261D'
sos = u'\U0001F198'
new = u'\U0001F195'
exclamation = u'\U00002757'
double_exclamation = u'\U0000203C'
check = u'\U00002714'
arrow = u'\U000027A1'
heart = u'\U00002764'

tb_token = '407083820:AAFB66RmIckJ1H46Uz_rmvR55pbVRPy5f_I'

bot = telebot.TeleBot(tb_token)


class LavaGame:
    def __init__(self, player_id, channel_id):
        self.players = []
        self.player_id = player_id
        self.channel_id = channel_id
        self.repeat = 1
        self.max_burn_time = 3
        self.max_safe_time = 3
        self.max_wave_time = 30
        self._lava_timer = 0
        self._wave_timer = 0
        self._random_num = 0

    def add_player(self, player_id):
        self.players.append(player_id)
        print(self.players)
        print(type(self))

    def send_messages(self, message):
        [bot.send_message(player, message) for player in self.players]

    def wave_time(self, w_time):
        if w_time > 300:
            w_time = 300
        self.max_wave_time = w_time
        self.send_messages('Maximum wave time is {} now'.format(self.max_wave_time))

    def safe_time(self, s_time):
        if s_time > 10:
            s_time = 10
        self.max_safe_time = s_time
        self.send_messages('Safe time is {} now'.format(self.max_safe_time))

    def burn_time(self, b_time):
        if b_time > 10:
            b_time = 10
        self.max_burn_time = b_time
        self.send_messages('Burning time is {} now'.format(self.max_burn_time))

    def repeats(self, repeat):
        if repeat > 10:
            repeat = 10
        self.repeat = repeat
        self.send_messages('Game will be repeated {} times'.format(self.repeat))

    def start_game(self):
        print(self.players)
        for i in range(self.repeat):
            self.wave_timer()

    def empty_func(self):
        pass

    def lava_coming(self):
        self.send_messages('Hide' + exclamation + '\nLava is coming after:')

        for sec in range(self.max_safe_time, 0, -1):
            self._lava_timer = threading.Timer(1, self.send_messages(str(sec)))
            self._lava_timer.start()
            self._lava_timer.join()

        self.send_messages('The floor is lava' + double_exclamation)

        for sec in range(0, self.max_burn_time, 1):
            self._lava_timer = threading.Timer(1, self.send_messages(fire * 11))
            self._lava_timer.start()
            self._lava_timer.join()

        self.send_messages('The floor is safe now')

    def wave_timer(self):
        for sec in range(self.max_wave_time, 0, -1):
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
    bot.send_message(message.chat.id,
                     'Hi! ' + smile + '\n'
                     'I\'m \"The floor is lava\" game. Let\'s play!' + fire + '\n\n'
                     '/host - create room ' + new + '\n'
                     '/join - join room ' + arrow + '\n'
                     '/play - start the game! ' + check + '\n'
                     '/help - if you want to change game options, call help! ' + sos + '\n\n'
                     'Remember!' + point + '\n'
                     'Only host of the room can change the game options and start the game! Good luck.' + heart)


@bot.message_handler(commands=['help'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     'Here is some commands for changing game options.\n\n'
                     '/time - maximum time of waves ' + watch + ' (std. - 30, max. - 300)\n'
                     '/safe - safe time before lava is coming ' + hourglass + ' (std. - 3, max. - 10)\n'
                     '/burn - burning lava time ' + fire + ' (std. - 3, max. - 10)\n'
                     '/repeat - repeats of coming lava waves ' + recycling + ' (std. - 1, max. - 10)\n\n'
                     'Remember that you can\'t stop the game while lava is coming, change options carefully!')


@bot.message_handler(commands=['host'])
def handle_start(message):
    try:
        channel_id = str(message.text).split()[-1]
        games[str(message.chat.id)] = LavaGame(message.chat.id, channel_id)
        games[str(message.chat.id)].add_player(message.chat.id)
        print(games[str(message.chat.id)])
        bot.send_message(message.chat.id, 'Game has been created with id: {}'.format(channel_id))
    except:
        bot.send_message(message.chat.id, 'Oh, something went wrong :c\n'
                                          'Don`t worry and try again!')


@bot.message_handler(commands=['join'])
def handle_start(message):
    try:
        channel_id = str(message.text).split()[-1]
        games[host_id(games, channel_id)].player_id = message.chat.id
        games[host_id(games, channel_id)].add_player(message.chat.id)
        print(games[host_id(games, channel_id)])
        bot.send_message(message.chat.id, 'You have been joined in room: {}'.format(channel_id))
    except:
        bot.send_message(message.chat.id, 'Oh, something went wrong :c\n'
                                          'Don`t worry and try again!')


@bot.message_handler(commands=['time'])
def handle_start(message):
    try:
        w_time = str(message.text).split()[-1]
        if is_host(message.chat.id):
            games[str(message.chat.id)].wave_time(int(w_time))
        else:
            bot.send_message(message.chat.id, 'Only host can set time!')
    except:
        bot.send_message(message.chat.id, 'Oh, something went wrong :c\n'
                                          'Don`t worry and try again!')


@bot.message_handler(commands=['safe'])
def handle_start(message):
    try:
        s_time = str(message.text).split()[-1]
        if is_host(message.chat.id):
            games[str(message.chat.id)].safe_time(int(s_time))
        else:
            bot.send_message(message.chat.id, 'Only host can set safe time!')
    except:
        bot.send_message(message.chat.id, 'Oh, something went wrong :c\n'
                                          'Don`t worry and try again!')


@bot.message_handler(commands=['burn'])
def handle_start(message):
    try:
        b_time = str(message.text).split()[-1]
        if is_host(message.chat.id):
            games[str(message.chat.id)].burn_time(int(b_time))
        else:
            bot.send_message(message.chat.id, 'Only host can set burning time!')
    except:
        bot.send_message(message.chat.id, 'Oh, something went wrong :c\n'
                                          'Don`t worry and try again!')


@bot.message_handler(commands=['repeat'])
def handle_start(message):
    try:
        iter = str(message.text).split()[-1]
        if is_host(message.chat.id):
            games[str(message.chat.id)].repeats(int(iter))
        else:
            bot.send_message(message.chat.id, 'Only host can set repeats of the game!')
    except:
        bot.send_message(message.chat.id, 'Oh, something went wrong :c\n'
                                          'Don`t worry and try again!')


@bot.message_handler(commands=['play'])
def handle_start(message):
    try:
        if is_host(message.chat.id):
            games[str(message.chat.id)].start_game()
        else:
            bot.send_message(message.chat.id, 'Only host can start the game!')
    except:
        bot.send_message(message.chat.id, 'Oh, something went wrong :c\n'
                                          'Don`t worry and keep calm')


if __name__ == '__main__':
    bot.polling(none_stop=True)
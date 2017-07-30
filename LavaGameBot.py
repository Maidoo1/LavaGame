'''
'The floor is lava' game for Telegram

Maidoo
31.07.17
'''

import telebot

tb_token = '407083820:AAFB66RmIckJ1H46Uz_rmvR55pbVRPy5f_I'

bot = telebot.TeleBot(tb_token)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Привет, для создания комнаты введи \\host, для присоединения к комнате введи \\join')

if __name__ == '__main__':
    bot.polling(none_stop=True)
import logging

from telegram import Update, Bot, InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
from telegram.ext import CommandHandler, Updater, MessageHandler, filters, InlineQueryHandler, CallbackQueryHandler
from typing import Tuple, Dict, Any, List
from tree_structure import Node
from functools import reduce
from tree import Tree

# ToDo
# 1. По команде `/start` бот присылает сообщение, где кнопки представлены в виде директорий.
# 2. Есть кнопка назад, которая возвращает нас на директорию "выше"
# 3. В узлах находятся кнопки, которые отркрывают url
# 4. Все сообщения должны работать независимо друг от друга
# * Если будут проблемы с параметрами, спрашивать меня или курить документацию

class MyBot:
    def __init__(self, token: str, tree_dict: dict):
        self.root = Node()
        self.tree = Tree(tree_dict)

        self.tree_redo()
        self.updater: Updater = Updater(token)
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start_callback))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.callback_query_callback))
    
    def start_callback(self, bot: Bot, update: Update):
        print(self.tree._nodes)
        markup = Markup([[Button(text=str(self.tree.get(uid=1)), callback_data=str(1))]])
        bot.send_message(chat_id=update.message.chat_id, text="Hello. It's zontik.ru", reply_markup=markup)
    
    def callback_query_callback(self, bot: Bot, update: Update):
        callback = int(update.callback_query.data)
        lst_btn = list()
        all_btn = list()
        if callback != -1:
            for child in self.tree.get(callback).children:
                if child.url is not None:
                    lst_btn.append(Button(text=child.__str__(), url=child.url, callback_data=callback))
                else:
                    lst_btn.append(Button(text=child.__str__(), callback_data=self.tree.find_uid(child.__str__())))
            all_btn.append(lst_btn)

            all_btn.append([Button(text='назад', callback_data=str(self.tree.find_parent(callback)))])
        else:
            all_btn.append([Button(text=str(self.tree.get(uid=1)), callback_data=str(1))])

        markup = Markup(all_btn)
        message = update.effective_message
        message_id = update.effective_message.message_id
        telegram_id = update.effective_chat.id
        bot.edit_message_reply_markup(reply_markup=markup, message_id=message_id, chat_id=telegram_id)

    def start_bot(self):
        self.updater.start_polling()

    def tree_redo(self, node: Node = None):
        pass


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    MyBot("701721190:AAEtlb05Fbi7VO9jRaOd6TARNv-kYhQj-ys",
          {'Корень': {'Зонтики': {"Зонтик 1": "https://www.google.ru/", "Зонтик2": "https://yandex.ru/",
                                  '1':{'2':{'3':'https://habr.com/ru/post/423987/'}}}, 'Kуртки': {'куртка1': 'https://www.google.ru/'}}}).start_bot()

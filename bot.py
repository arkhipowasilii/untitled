import logging

from telegram import Update, Bot, InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
from telegram.ext import CommandHandler, Updater, MessageHandler, filters, InlineQueryHandler, CallbackQueryHandler
from typing import Tuple, Dict, Any, List

from keyboard_builder import KeyboardBuilder
from node import Node
from functools import reduce
from tree import Tree
import json


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
        markup = Markup([[Button(text=str(self.tree.get(uid=1)), callback_data=str(1))]])
        bot.send_message(chat_id=update.message.chat_id, text="Hello. It's zontik.ru", reply_markup=markup)

    def callback_query_callback(self, bot: Bot, update: Update):
        # ToDo Если элементов в строке больше 4-х, делать две строки итд
        current_node: int = int(update.callback_query.data)

        # kb = KeyboardBuilder(callback, self.tree).element_in_line(4)
        kb = KeyboardBuilder()
        node = self.tree.get(current_node)


        markup = Markup(kb)
        message = update.effective_message
        message_id = update.effective_message.message_id
        telegram_id = update.effective_chat.id
        bot.edit_message_reply_markup(reply_markup=markup, message_id=message_id, chat_id=telegram_id)

    def start_bot(self):
        self.updater.start_polling()

    def tree_redo(self, node: Node = None):
        pass


if __name__ == '__main__':
    with open("menu.json", "r", encoding="utf-8") as write_file:
        menu_dict = json.load(write_file)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    MyBot("701721190:AAEtlb05Fbi7VO9jRaOd6TARNv-kYhQj-ys",
          menu_dict).start_bot()

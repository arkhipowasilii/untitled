import logging

from telegram import Update, Bot, InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup
from telegram.ext import CommandHandler, Updater, MessageHandler, filters, InlineQueryHandler, CallbackQueryHandler
from typing import Tuple, Dict, Any, List
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

class KeyboardBuilder:
    # TODO Builder Pattern
    def __init__(self):
        self._element_in_line = None

    def element_in_line(self, elements: int):
        self._element_in_line = elements
        return self

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
        # ToDo Если элементов в строке больше 4-х, делать две строки итд

        callback = int(update.callback_query.data)
        lst_btn, all_btn = list(), list()

        kb = KeyboardBuilder().element_in_line(10)
        
        if callback != -1:
            for child in self.tree.get(callback).children:
                if child.url is not None:
                    lst_btn.append(Button(text=str(child), url=child.url, callback_data=callback))
                else:
                    lst_btn.append(Button(text=str(child), callback_data=self.tree.find_uid(str(child))))

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

    with open("menu.json", "r", encoding="utf-8") as write_file:
        menu_dict = json.load(write_file)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    MyBot("701721190:AAEtlb05Fbi7VO9jRaOd6TARNv-kYhQj-ys",
          menu_dict).start_bot()

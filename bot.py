
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
    def __init__(self, callback_num: int, tree: Tree):
        self._element_in_line = None
        self.callback_node = None
        self.callback_num = callback_num
        self.tree = tree
        if callback_num != -1:
            self.callback_node = self.tree.get(self.callback_num)

    def element_in_line(self, elements: int) -> [[Button]]:
        if self.callback_node is not None:
            max_index = len(self.callback_node.children) / elements
            if max_index != int(max_index):
                max_index += 1
            all_btns = []

            for index in range(int(max_index)):
                current_lst_btns = []

                for child in parting(self.callback_node.children, elements, index):
                    if child.url is not None:
                        current_lst_btns.append(Button(text=str(child), url=child.url, callback_data=str(self.callback_node._uid)))
                    else:
                        current_lst_btns.append(Button(text=str(child), callback_data=str(child._uid)))

                all_btns.append(current_lst_btns)

            all_btns.append([Button(text='назад', callback_data=str(self.tree.find_parent(self.callback_num)))])
        else:
            return [[Button(text=str(self.tree.get(uid=1)), callback_data=str(1))]]

        return all_btns


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
        callback = int(update.callback_query.data)

        kb = KeyboardBuilder(callback, self.tree).element_in_line(4)

        markup = Markup(kb)
        message = update.effective_message
        message_id = update.effective_message.message_id
        telegram_id = update.effective_chat.id
        bot.edit_message_reply_markup(reply_markup=markup, message_id=message_id, chat_id=telegram_id)

    def start_bot(self):
        self.updater.start_polling()

    def tree_redo(self, node: Node = None):
        pass


def parting(lst: List, part_len: int, num_element: int) -> List:
    result_lst = [lst[part_len * k:part_len * (k + 1)] for k in range(len(lst) // part_len + 1)]

    if len(result_lst[-1]) == 0:
        del result_lst[-1]

    return result_lst[num_element]


if __name__ == '__main__':
    with open("menu.json", "r", encoding="utf-8") as write_file:
        menu_dict = json.load(write_file)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    MyBot("701721190:AAEtlb05Fbi7VO9jRaOd6TARNv-kYhQj-ys",
          menu_dict).start_bot()

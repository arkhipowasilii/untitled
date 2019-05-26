from math import ceil

from telegram import InlineKeyboardButton as Button

from bot import parting
from node import Node
from tree import Tree


class KeyboardBuilder:
    def __init__(self):
        pass

    def element_in_line(self, elements: int) -> [[Button]]:
        if self.callback_node is None:
            return [[Button(text=str(self.tree.get(uid=1)), callback_data=str(1))]]

        buttons = []

        nodes = self.callback_node.children

        lines = [nodes[elements * line_number : elements * (line_number + 1)]
            for line_number in range(len(nodes) // elements + 1)]

        for line in lines:
            buttons.append(list(map(self.button, line)))

        buttons.append([Button(text='назад', callback_data=str(self.tree.find_parent(self.callback_num)))])

        return buttons

    @staticmethod
    def button(node: Node, parent_uid: int):
        if node.url is not None:
            return Button(text=str(node), url=node.url, callback_data=str(parent_uid))

        return Button(text=str(node), callback_data=str(node._uid))


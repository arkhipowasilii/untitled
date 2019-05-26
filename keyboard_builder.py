from telegram import InlineKeyboardButton as Button

from bot import parting
from tree import Tree


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
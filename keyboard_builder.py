from math import ceil
from typing import Callable, Any, Tuple, List, Optional

from telegram import InlineKeyboardButton as Button, InlineKeyboardMarkup


class KeyboardBuilder:
    # ToDo Перенести логику раскидывания кнопок по линиям на `button`
    def __init__(self):
        self._preprocess = lambda data: (str(data), str(data), None)
        self._inline_count = None
        self._buttons: List[List[Button]] = [[]]

    def set_preprocess(self, preprocess: Callable[[Any], Tuple[str, str, str]]):
        self._preprocess = preprocess
        return self

    def elements_in_line(self, count: int) -> [[Button]]:
        self._inline_count = count
        return self

    def button(self, data: Any):
        data, callback, url = self._preprocess(data)
        current_button = Button(text=data, callback_data=callback, url=url)

        for index in range(len(self._buttons)):
            if len(self._buttons[index]) >= self._inline_count:
                try:
                    if len(self._buttons[index+1]) >= self._inline_count:
                        continue
                    else:
                        self._buttons[index+1].append(current_button)
                except:
                    self._buttons[index+1] = [current_button]
            else:
                self._buttons[index].append(current_button)
        return self

    def line(self) -> 'KeyboardBuilder':
        # ToDo Homework
        raise NotImplementedError()

    def back(self, callback_data: str):
        self._buttons.append(Button(text="<-", callback_data=callback_data))
        return self

    def get(self) -> InlineKeyboardMarkup:
        buttons = [self._buttons[self._inline_count * line: self._inline_count * (line + 1)]
                   for line in range(ceil(len(self._buttons) // self._inline_count))]

        return InlineKeyboardMarkup(buttons)

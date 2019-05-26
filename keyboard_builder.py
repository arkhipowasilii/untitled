from math import ceil
from typing import Callable, Any, Tuple, List, Optional

from telegram import InlineKeyboardButton as Button, InlineKeyboardMarkup


class KeyboardBuilder:
    # ToDo Перенести логику раскидывания кнопок по линиям на `button`
    def __init__(self):
        self._preprocess = lambda data: (str(data), str(data), None)
        self._inline_count = None
        self._buttons: List[Button] = []

    def set_preprocess(self, preprocess: Callable[[Any], Tuple[str, str, str]]):
        self._preprocess = preprocess
        return self

    def elements_in_line(self, count: int) -> [[Button]]:
        self._inline_count = count
        return self

    def button(self, data: Any):

        data, callback, url = self._preprocess(data)
        self._buttons.append(Button(text=data, callback_data=callback, url=url))

        return self

    def line(self) -> 'KeyboardBuilder':
        raise NotImplementedError()

    def back(self, callback_data: str):
        self._buttons.append(Button(text="<-", callback_data=callback_data))
        return self

    def get(self) -> InlineKeyboardMarkup:
        buttons = [self._buttons[self._inline_count * line : self._inline_count * (line + 1)]
            for line in range(ceil(len(self._buttons) // self._inline_count))]

        return InlineKeyboardMarkup(buttons)

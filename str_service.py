import logging
from collections import namedtuple
from typing import Union, List, Optional, Dict

from node import Node


def _get_difference(request: str, data: Union[Node, str]) -> str:
    """

    :param request:
    :param data:
    :return:
    """
    return " ".join(list(filter(lambda word: get_distance(str(data), word) > 2, request.split(' '))))


def get_distance(left_word: str, right_word: str) -> int:
    '''

    :param left_word:
    :param right_word:
    :return:
    '''
    # ToDo Протестировать функцию
    # FixMe ТУТ ЕСТЬ ОШИБКИ
    # FixMe ИХ НАДО ИСПРАВИТЬ

    assert left_word.find(' ') == -1
    assert right_word.find(' ') == -1

    len_left, len_right = len(left_word), len(right_word)

    if len_right == 0 or len_left == 0:
        return len_right + len_left

    if len_left > len_right:
        left_word, right_word = right_word, left_word
        len_left, len_right = len_right, len_left

    _matrix: List[List[Optional[int]]] = list(list(0 for _ in range(len_left + 1)) for _ in range(len_right + 1))

    for right_index in range(1, len_right + 1):
        for left_index in range(1, len_left + 1):

            if right_index == 1:
                _matrix[0][left_index] = left_index

            if left_index == 1:
                _matrix[right_index][0] = right_index

            add = _matrix[right_index][left_index - 1] + 1
            delete = _matrix[right_index - 1][left_index] + 1
            change = _matrix[right_index - 1][left_index - 1]
            if right_word[right_index - 1] != left_word[left_index - 1]:
                change += 1

            _matrix[right_index][left_index] = min(add, delete, change)

    return _matrix[-1][-1]


DifferencePoint = namedtuple("Diff", ("word", "distance"))


def _get_difference_point(data: Union[Node, str], request: str) -> DifferencePoint:
    """

    :param data:
    :param request:
    :return:
    """

    data = str(data)
    min_dis = len(data)
    result = None

    for request_word in request.split(' '):
        distance = get_distance(request_word, data)
        if distance < min_dis:
            min_dis, result = distance, request_word

    return DifferencePoint(word=result, distance=min_dis)


def _get_intersection(right_word: str, left_word: str):
    len_left, len_right = len(left_word), len(right_word)
    if len_left > len_right:
        left_word, right_word = right_word, left_word
        len_left, len_right = len_right, len_left
    if left_word in right_word:
        return left_word
    for index in range(len_left):
        for index2 in range(len_left - (len_left - index) + 1):
            left_slice = left_word[index2:: (len_left - index)]
            logging.debug(f"left_slice --> {left_slice}")
            if left_slice in right_word:
                return left_slice


if __name__ == '__main__':
    print(get_distance('KlrxT', 'KlgtT'))

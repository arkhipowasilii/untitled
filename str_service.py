import logging
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
    # ToDo Разобрать док-о алгоритма

    assert left_word.find(' ') == -1
    assert right_word.find(' ') == -1

    len_left, len_right = len(left_word), len(right_word)

    if len_right == 0 or len_left == 0:
        return len_right + len_left

    if len_left > len_right:
        left_word, right_word = right_word, left_word
        len_left, len_right = len_right, len_left

    _matrix: List[List[Optional[int]]] = list(list(0 for _ in range(len_left)) for _ in range(len_right))

    for right_index in range(len_right):
        for left_index in range(len_left):

            if right_index == 0:
                _matrix[0][left_index] = left_index
                continue

            if left_index == 0:
                _matrix[right_index][0] = right_index
                continue

            add = _matrix[right_index][left_index - 1]
            delete = _matrix[right_index - 1][left_index]
            change = _matrix[right_index - 1][left_index - 1]
            if right_word[right_index] != left_word[left_index]:
                change += 1

            _matrix[right_index][left_index] = min(add, delete, change)

    return _matrix[-1][-1]


def _get_difference_point(data: Union[Node, str], request: str) -> Dict[str, Union[str, int]]:
    '''

    :param data:
    :param request:
    :return:
    '''
    # ToDo 2 Normal intersection
    data = str(data)
    min_dis = result = len(data)

    for request_word in request.split(' '):
        request_distance = get_distance(request_word, data)
        if request_distance < min_dis:
            min_dis, result = request_distance, request_word

    return {"word": result, "distance": min_dis}


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

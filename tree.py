import logging
from typing import Tuple, Union, Optional, List, Dict
import json
from node import Node


# ToDo Homework make tests for `Tree` class.

class Tree:
    def __init__(self, tree_dict: dict):
        assert len(tree_dict.keys()) == 1
        key = tuple(tree_dict.keys())[0]

        self.root = Node(name=key)

        self._nodes = dict()

        self.add_uid(self.root)

        self.add(self.root, tree_dict[key])

    def add_uid(self, node: Node):
        self._nodes[node.uid] = node

    def add(self, node: Node, raw_data: dict):

        for key, value in raw_data.items():
            if isinstance(value, str):
                new_node = Node(name=key, url=value)
                node.add_child(new_node)
                self.add_uid(new_node)

            elif isinstance(value, dict):
                new_node = Node(name=key)
                node.add_child(new_node)
                self.add_uid(new_node)
                self.add(new_node, value)

            else:
                raise ValueError(f"{value}")

    def get(self, uid: int) -> Node:
        return self._nodes[uid]

    def find_uid(self, name: str) -> int:
        for uid, node in self._nodes.items():
            if node.__str__() == name:
                return uid

    def all_uid(self):
        return [node.uid() for node in self._nodes.values()]

    def find_parent(self, uid: int) -> int:
        uid1 = None
        for node in self._nodes.values():
            if self.get(uid) in node.children:
                uid1 = node.uid
        if uid1 is None:
            return -1
        return uid1

    def find(self, request: str) -> Union[Node, Tuple[Node], None]:
        paths = self._find(self.root, request)

        if any(weight == 0 for weight, _ in paths):
            return paths[-1][1]

        path = min(paths, key=lambda weight_path: weight_path[0])
        return path[-1][1]

    def _find(self, node: Node, request: str, weight: int = None) -> List[Tuple[int, Node]]:
        """
        Возвращает узел, если поиск успешен
        Возвращает все не отверженные пути, если поиск не успешен и взвешивает их
        :param node:
        :param request:
        :return:
        """

        weight = weight or 0

        if len(request) == 0:
            return [(0, node), ]

        if node.is_leaf:
            # ToDo Add request
            return [(len(request.split(' ')), node), ]

        node_weights: Tuple[Tuple[Node, dict]] = tuple((child, _get_difference_point(child, request))
                                                       for child in node.children)

        logging.debug(f"node_weights --> {node_weights}")

        nodes: Tuple[Tuple[Node, dict]] = sorted(node_weights,
                                                 key=lambda node_data: node_data[1]['distance'])

        logging.debug(f"nodes --> {nodes}")

        def _find_path(child: Node, intersection: str, weight_child: int) -> tuple:
            return child, \
                   self._find(child, _get_difference(request, intersection), weight + weight_child)

        current_paths = []
        for child, paths in (_find_path(node, data['word'], data['distance']) for node, data in nodes):
            for path_weight, path in paths:
                if len(path) != 1:
                    path.append(child)

                current_paths.append((path_weight, path))

        if any(pair[0] == 0 for pair in current_paths):
            current_paths = list(filter(lambda pair: pair[0] == 0, current_paths))

        return current_paths


def _get_difference(request: str, data: Union[Node, str]) -> str:
    """

    :param request:
    :param data:
    :return:
    """
    return " ".join(list(filter(lambda word: distance(str(data), word) > 2, request.split(' '))))


def distance(left_word: str, right_word: str) -> int:
    '''

    :param left_word:
    :param right_word:
    :return:
    '''
    # ToDo Протестировать функцию
    # ToDo_less Разобрать док-о алгоритма

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

            if left_index == 0:
                _matrix[right_index][0] = right_index

            add = _matrix[right_index][left_index - 1] + 1
            delete = _matrix[right_index - 1][left_index] + 1
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
    min_dis, result = len(data)

    for request_word in request.split(' '):
        request_distance = distance(request_word, data)
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    with open("menu.json", "r", encoding="utf-8") as write_file:
        menu_dict = json.load(write_file)
    print(_get_intersection("abcbsjh", "qqabcx"))
    example_tree = Tree(menu_dict)

import logging
from typing import Tuple, Union, Optional, List, Dict
import json
from node import Node


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

    def find1(self, name: str):
        return self.root.find(name)

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
        global result_paths
        result_paths = list()
        paths = self._find(self.root, request)
        if len(paths) == 1:
            return paths[0]
        elif len(paths) == 0:
            return None
        else:
            return paths

    def _find(self, node: Node, request: str) -> Tuple[Node]:
        """
        Возвращает узел, если поиск успешен
        Возвращает все не отверженные пути, если поиск не успешен и взвешивает их
        :param node:
        :param request:
        :return:
        """
        if len(request) == 0:
            return node,

        if node.is_leaf:
            return node,

        node_weights: Tuple[Tuple[Node, str]] = tuple((child, _get_intersection(child, request))
                                                      for child in node.children)
        logging.debug(f"node_weights --> {node_weights}")
        nodes: Tuple[Tuple[Node, str]] = sorted(node_weights, key=lambda pair: len(pair[1]))
        print(f"nodes --> {nodes}")

        def _find_path(child, intersection):
            return child, self._find(child, _get_difference(request, intersection))

        paths: List[float, Tuple[Node]] = list()
        for child, path in map(_find_path, nodes):
            if len(path) == 1:
                return path

            weight = None  # TODO HERE

            path = list(path)
            path.append(child)

            paths.append((weight, path))

        return paths


def _get_difference(request: str, data: Union[Node, str]) -> str:
    '''

    :param request:
    :param data:
    :return:
    '''
    return " ".join(list(filter(lambda word: _distance(str(data), word) > 2, request.split(' '))))


def _distance(left_word: str, right_word: str) -> int:
    '''

    :param left_word:
    :param right_word:
    :return:
    '''
    # ToDo Протестировать функцию
    # ToDo_less Разобрать док-о алгоритма

    len_left, len_right = len(left_word), len(right_word)

    if len_left > len_right:
        left_word, right_word = right_word, left_word
        len_left, len_right = len_right, len_left

    assert left_word.find(' ') == -1
    assert right_word.find(' ') == -1

    _matrix: List[List[Optional[int]]] = list(list(None for _ in range(len_left)) for _ in range(len_right))

    for right_index, right_char in enumerate(right_word):
        for left_index, left_char in enumerate(left_word):

            if right_index == 0:
                _matrix[0][left_index] = left_index

            if left_index == 0:
                _matrix[right_index][0] = right_index

            add = _matrix[right_index][left_index - 1]
            delete = _matrix[right_index - 1][left_index]
            change = _matrix[right_index - 1][left_index - 1]

            if right_word[right_index] != left_word[left_index]:
                change += 1

            _matrix[left_index][right_index] = min(add, delete, change)

    return _matrix[-1][-1]


def _get_intersection(data: Union[Node, str], request: str) -> set:
    '''

    :param data:
    :param request:
    :return:
    '''
    # ToDo 2 Normal intersection
    data = str(data)
    minimum_inter = len(data)

    for request_word in request.split(' '):
        request_distance = _distance(request_word, data)
        if request_distance < minimum_inter:
            minimum_inter = request_distance

    return minimum_inter


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    with open("menu.json", "r", encoding="utf-8") as write_file:
        menu_dict = json.load(write_file)

    ex_tree = Tree(menu_dict)
    print(_get_difference("Зоктики", "зонтики"))
    print(ex_tree.find("зззззз2"))

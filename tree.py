from typing import Tuple, Union

from node import Node

class Tree:
    def __init__(self, tree_dict: dict):
        assert len(tree_dict.keys()) == 1
        key = tuple(tree_dict.keys())[0]

        self.root = Node(name=key)

        self._nodes = dict()

        self.add_uid(self.root)

        # ToDo 3 Add sorting of data by lexicographical for children layer
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
        paths = self._find(self.root, request)
        if len(paths) == 1:
            return paths[0]
        elif len(paths) == 0:
            return None
        else:
            return paths

    def _find(self, node: Node, request: str) -> Tuple[Node]:

        if len(request) == 0:
            return node,

        if node.is_leaf:
            return node,

        node_weights = ((child, _get_intersection(child, request)) for child in node.children)

        nodes: Tuple[Tuple[Node, str]] = sorted(node_weights, key=lambda pair: len(pair[1]))

        paths: Tuple[Tuple[Node]] = (self._find(node, _get_difference(request, intersection))
                                                                for node, intersection in nodes)

        # ToDo add return with use generator logic
        result = []

        for path in paths:
            pass

        return result

def _get_difference(request: str, data: Union[Node, str]) -> str:
    '''

    :param request:
    :param data:
    :return:
    '''
    intersection = _get_intersection(str(data), request)
    return " ".join(list(filter(lambda word: _distance(intersection, word) > 2, request.split(' '))))

def _distance(left_word:str, right_word:str) -> int:
    '''

    :param left_word:
    :param right_word:
    :return:
    '''
    # ToDo Изучить Рас-е Левенштейна и отрефакторить данную функцию и объяснить мне её

    len_left, len_right = len(left_word), len(right_word)
    if len_left > len_right:
        left_word, right_word = right_word, left_word
        len_left, len_right = len_right, len_left

    current_row = range(len_left+1) # Keep current and previous row, not entire matrix
    for index in range(1, len_right+1):

        previous_row, current_row = current_row, [index]+[0] * len_left
        for inner_index in range(1,len_left+1):
            add, delete, change = previous_row[inner_index]+1, current_row[inner_index-1]+1, previous_row[inner_index-1]

            if left_word[inner_index - 1] != right_word[index - 1]:
                change += 1

            current_row[inner_index] = min(add, delete, change)

    return current_row[len_left]

def _get_intersection(data: Union[Node, str], request: str) -> str:
    '''

    :param data:
    :param request:
    :return:
    '''
    # ToDo 2 Normal intersection
    data = str(data)
    word, distance = "", None

    for request_word in request.split(' '):
        request_distance = _distance(data, request_word)

        if request_distance > 2:
            continue

        if distance is None or request_distance < distance:
            word, distance = data, request_distance

    return word


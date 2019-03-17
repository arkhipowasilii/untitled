from typing import Tuple, Union

from node import Node
from functools import reduce


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

        node_weights = {child: len(_get_intersection(child, request))
                            for child in node.children}

        max_weight = max(node_weights.values())

        nodes = tuple(node for node, weight in node_weights.items()
                                        if weight == max_weight)

        paths: Tuple[Tuple[Node]] = tuple(self._find(node, _get_difference(node, request)) for node in nodes)
        print(paths)
        print(request)
        # ToDo If we haven't got correct (with `len() == 1`) paths, we must return path with max relevant
        if len(paths) ==1:
            return tuple(path[0] for path in paths if len(path) == 1)
        else:
            return paths[1]


def _get_difference(node: Node, request: str) -> str:
    '''

    :param node:
    :param request:
    :return: Return `request \ node.data`
    '''
    # ToDo 1 Normal difference (spell-mistake delta 2)
    node_name = set(node.__str__())
    result_dict = dict()
    for word_req in request.split(' '):
        difference = node_name.intersection(set(word_req))
        if len(difference) >= len(node_name) - 2:
            result_dict[len(difference)] = word_req
    if len(result_dict) == 0:
        return request
    max = reduce(lambda a, b: a if (a > b) else b, result_dict.keys())
    return request.replace(result_dict[max], '').replace('  ', ' ')


def _get_intersection(node: Node, request: str) -> str:
    '''

    :param node:
    :param request:
    :return:
    '''
    # ToDo 2 Normal intersection
    node_name = set(node.__str__())
    result_dict = dict()
    for word_req in request.split(' '):
        intersection = node_name.intersection(set(word_req))
        result_dict[len(intersection)] = intersection
    max = reduce(lambda a, b: a if (a>b) else b, result_dict.keys())
    return result_dict[max]


if __name__ == "__main__":
    tr = Tree({'Корень': {'Зонтики': {"Зонтик1": "https://www.google.ru/",'1': {'2': {'3': 'https://habr.com/ru/post/423987/'}}, "Зонтик2": "https://yandex.ru/"},
                          'Kуртки': {'куртка1': 'https://www.google.ru/'}}})
    print(tr.find('Зонтик1 p'), '<-- res')

from typing import Callable, List

from tree_structure import Node
from copy import copy

class Tree:
    def __init__(self, tree_dict: dict):
        assert len(tree_dict.keys()) == 1
        key = tuple(tree_dict.keys())[0]
        
        self.root = Node(name=key)
        
        self._nodes = dict()

        self.add_uid(self.root)
        self.add(self.root, tree_dict[key])

        #def func(node):
        #    self._nodes[node.uid] = node
        #
        #self.traversal(func)

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
    
    def find(self, name: str):
        return self.root.find(name)
    
    def get(self, uid: int) -> Node:
        return self._nodes[uid]

    def find_uid(self, name: str) -> int:
        for uid, node in self._nodes.items():
            if node.__str__() == name:
                return uid

    def all_uids(self):
        return [node.uid() for node in self._nodes.values()]

    def find_parent(self, uid: int) -> int:
        uid1 = None
        for node in self._nodes.values():
            if self.get(uid) in node.children:
                uid1 = node.uid
        if uid1 is None:
            return -1
        return uid1

    def get_nodes_weight(self, request: str):
        result = dict()
        for node in self._nodes.values():
            result[node] = _intersection(node, request)
        return result

    def clever_find(self, request: str) -> Node:
        node_weight = self.get_nodes_weight(request)
        maximum = max(node_weight.values())
        for key in node_weight.keys():
            if node_weight[key] == maximum:
                return key

    def clever_find1(self, request: str) -> Node:

        node_weight = self.get_nodes_weight(request)
        result = None

        def filter_(node: Node):
            level = node_weight[node]

            if level == 0:
                return False

            return max(node_weight.values()) == level

        def callback(node: Node):
            global result
            result = copy(node)

        self.root.traversal(filter_, callback)

        return result


def _intersection(node: Node, request: str) -> int:
    return len(set(node.name).intersection(request))


def return_node(node: Node) -> Node:
    return node


if __name__ == "__main__":
    tr = Tree({'Корень': {'Зонтики': {"Зонтик 1": "https://www.google.ru/", "Зонтик2": "https://yandex.ru/",
                                      '1': {'2': {'3': 'https://habr.com/ru/post/423987/'}}},
                          'Kуртки': {'куртка1': 'https://www.google.ru/'}}})
    print(tr.clever_find1('крутк'))
    print(tr.clever_find('корен'))

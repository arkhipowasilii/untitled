from typing import Callable

from tree_structure import Node


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

    def find_parent(self, uid: int) -> int:
        uid1 = None
        for node in self._nodes.values():
            if self.get(uid) in node.children:
                uid1 = node.uid
        if uid1 is None:
            return -1
        return uid1

    def traversal(self, callback: Callable[[Node], None]) -> Node:
        pass

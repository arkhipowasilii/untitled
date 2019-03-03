from typing import Iterable, Optional


class Node:
    _global_register = 0
    
    def __init__(self, name: str='root', children: Iterable['Node']=None, url: str = None):
        self._uid = self._global_register
        Node._global_register += 1
        
        self.name: str = name
        self.url: str = url
        self.children = list()
        if children:
            assert all(isinstance(child, Node) for child in children)
            self.children = list(children)
    
    @property
    def uid(self) -> int:
        return self._uid

    def __repr__(self):
        return f"{self._uid}::{self.name}::{self.url}::{','.join(tuple(str(child.uid) for child in self.children))}"

    def __str__(self):
        return self.name

    def add_child(self, node: 'Node'):
        assert isinstance(node, Node)
        self.children.append(node)

    def add_children(self, lst_node: Iterable['Node']):
        for node in lst_node:
            self.add_child(node)

    def find(self, node_name: str) -> Optional['Node']:
        if self.name == node_name:
            return self
        
        for child in self.children:
            if child.name == node_name:
                return child
        
        for child in self.children:
            result = child.find(node_name)
            if result:
                return result
        
        return None


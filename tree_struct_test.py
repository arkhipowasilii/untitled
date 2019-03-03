import pytest

from tree import Tree
from tree_structure import Node


def test_tree():
    raw = {'Корень': {'Зонтики': {"Зонтик 1": "https:\\zontik.ru", "Зонтик2": "https:\\zontik2.ru"}, 'Kуртки': {
        'куртка1': '11'}}}
    tree = Tree(raw)
    print(tree.find('Корень').__repr__())
    print(tree._nodes)
    print(tree.get(0))
    print(tree.find_parent(0))



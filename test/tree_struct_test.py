import pytest

from tree import Tree
from node import Node


def test_tree():
    raw = {'Корень': {'Зонтики': {"Зонтик 1": "https:\\zontik.ru", "Зонтик2": "https:\\zontik2.ru"}, 'Kуртки': {
        'куртка1': 'https://habr.com/ru/post/423987/'}}}
    tree = Tree(raw)
    assert tree.root.__str__() == Node(name='Корень').__str__()
    assert tree._nodes[2].__str__() == "Зонтик 1"


def test_get():
    raw = {'Корень': {'Зонтики': {"Зонтик 1": "https:\\zontik.ru", "Зонтик2": "https:\\zontik2.ru"}, 'Kуртки': {
        'куртка1': 'https://habr.com/ru/post/423987/'}}}
    tree = Tree(raw)
    assert tree.get(5).__str__() == 'куртка1'
    assert tree.get(1).__str__() == 'Зонтики'

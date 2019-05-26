import string

from tree import Tree
from str_service import get_distance
from node import Node
from typing import List
from random import shuffle
import random
from create_random_tree import get_random_dict


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


def tes_distance():
    assert get_distance("abc", '') == 3
    assert get_distance("abc", "xabcq") == 2
    assert get_distance("qwerty", "qaerty") == 1


def get_random_path(node: Node) -> List[Node]:
    result_node = random.choice(node.children)

    if len(result_node.children) == 0:
        return [result_node, ]

    return [result_node, *get_random_path(result_node)]


def get_mixed_request(node_list: List[Node]) -> str:
    node_name_list = [node.name for node in node_list]
    shuffle(node_name_list)
    return " ".join(node_name_list)


def test_find():
    dict_depth = 7
    rnd_tree = Tree(get_random_dict(dict_depth))

    rnd_path = (get_random_path(rnd_tree.root))
    request = get_mixed_request(rnd_path)
    result = rnd_tree.find(request)
    # ToDo Fix error with depth level (at now: -1 level)
    pass

def test_sorting_nodes():
    dict_depth = 3

    tree = Tree(get_random_dict(dict_depth))


    for child in tree.root.children:
        child.name = f"data{''.join(tuple(random.choices(string.ascii_lowercase, k=10)))}"

    nodes = tree._sorting_children(tree.root, "data")
    assert len(nodes) == len(tree.root.children)
    for node, weight in nodes:
        assert weight.distance == 10
        assert weight.word == "data"

def test_sorting_nodes_2():
    dict_depth = 3

    tree = Tree(get_random_dict(dict_depth))

    request = ' '.join([random.choice(tree.root.children).name, random.choice(tree.root.children).name] + \
              list(''.join(random.choices(string.ascii_lowercase, k=10)) for _ in range(10)))

    nodes = tree._sorting_children(tree.root, request)
    # ToDo add asserts

def test_find_private():
    tree = Tree(get_random_dict(2))
    node = random.choice(tree.root.children)
    result = tree._find(tree.root, node.name, 0)
    pass

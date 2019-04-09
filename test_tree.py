from tree import Tree, distance
from node import Node
from typing import Tuple, List
from random import randint, shuffle
import pytest
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
    assert distance("abc", '') == 3
    assert distance("abc", "xabcq") == 2
    assert distance("qwerty", "qaerty") == 1


def test_find():
    dict_depth = 4
    example_dict = get_random_dict(dict_depth)
    example_tree = Tree(example_dict)

    def get_path(node: Node) -> List[Node]:
        random_num = randint(0, len(node.children)-1)

        for index in range(len(node.children)):
            if index == random_num:
                result_node = node.children[index]

                if len(result_node.children) == 0:
                    return [result_node]
                else:
                    result_list = list()
                    result_list = result_list + [result_node]
                    result_list = result_list + get_path(result_node)
                    return result_list

    def get_mixed_request(node_list: List[Node]) -> str:
        node_name_list = [node.name for node in node_list]
        print(node_name_list)
        return " ".join(node_name_list)

    res = (get_path(example_tree.root))
    print(res)
    print(get_mixed_request(res))

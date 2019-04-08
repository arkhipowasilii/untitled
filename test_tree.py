from tree import Tree, distance
from node import Node
from typing import Tuple
from random import randint
import pytest
from create_random_tree import get_random_dict


def tes_distance():
    assert distance("abc", '') == 3
    assert distance("abc", "xabcq") == 2
    assert distance("qwerty", "qaerty") == 1


def test_find():
    dict_depth = 3
    example_dict = get_random_dict(dict_depth)
    example_tree = Tree(example_dict)
    def get_path(node: Node, local_depth: int, dict_depth: int) -> Tuple[Node]:
        if local_depth > dict_depth:
            return
        else:

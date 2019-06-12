import logging
from collections import namedtuple
from typing import Tuple, Union, List
import json
from node import Node

# ToDo Homework make tests for `Tree` class.
from str_service import _get_difference, _get_difference_point


class Path:
    def __init__(self, node: Node = None, weight: int = None):
        self.nodes = [node, ] if node is not None else list()
        self.weight = weight or 0

    def __add__(self, other: Union['Path', Tuple[Node, int]]) -> 'Path':
        if isinstance(other, Path):
            for other_node in other.nodes:
                self.nodes.append(other_node)
            self.weight += other.weight

        elif isinstance(other, tuple):
            self.nodes += [other[0]]
            self.weight += other[1]

        return self

class Tree:
    def __init__(self, tree_dict: dict):
        assert len(tree_dict.keys()) == 1
        key = tuple(tree_dict.keys())[0]

        self.root = Node(name=key)

        self._nodes = dict()

        self.add_uid(self.root)

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
        paths = self._find(request)
        if any(weight == 0 for weight, _ in paths):
            return paths[-1][1]
        path = min(paths, key=lambda weight_path: weight_path[0])
        return path[-1][0]

    @classmethod
    def _sorting_children(cls, node: Node, request: str) -> Tuple[Tuple[Node, int]]:

        Pair = Tuple[Node, int]

        node_weights: Tuple[Pair] = tuple(Pair(node=child,
                                               weight=_get_difference_point(child, request))
                                          for child in node.children)

        node_weights = tuple(filter(lambda data: data.weight.word != None, node_weights))
        nodes: Tuple[Pair] = sorted(node_weights, key=lambda node_data: node_data.weight.distance)
        return nodes

    def _find(self, request: str, path: Path = None) -> Union[Path, List[Path]]:
        """
        TODO FIXME
        Возвращает узел, если поиск успешен
        Возвращает все не отверженные пути, если поиск не успешен и взвешивает их

        :param node:
        :param request:
        :return:
        """

        if path is None:
            path = Path(self.root)

        node = path.nodes[-1]

        if request == '' or node.is_leaf:
            return path

        paths = list()
        for child, dif_point in self._sorting_children(node, request):
            updated_request = _get_difference(request, child.name)
            path += self._find(updated_request, path)
            paths.append(path)
            # ToDo Realize this part of logic
            # Вызов поиска для child с "порезанным" request
            # Матчинг вывода find для child
            pass

        min_weight_path = None
        for current_path in paths:
            if min_weight_path is None:
                min_weight_path = current_path
            else:
                if min_weight_path.weight > current_path.weight:
                    min_weight_path = current_path

        if min_weight_path.weight < len(min_weight_path.nodes)*2:
            return min_weight_path

        # ToDo проверка на то, нет ли среди путей - корректного (`min(weight)`)

        if len(paths) == 1:
            return paths[0]

        return paths


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    with open("menu_test.json", "r", encoding="utf-8") as write_file:
        menu_dict = json.load(write_file)

    example_tree = Tree(menu_dict)
    print(example_tree.find("london camps"))

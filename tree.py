import logging
from typing import Tuple, Union, List
import json
from node import Node


# ToDo Homework make tests for `Tree` class.
from str_service import _get_difference, _get_difference_point


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
        paths = self._find(self.root, request)

        if any(weight == 0 for weight, _ in paths):
            return paths[-1][1]

        path = min(paths, key=lambda weight_path: weight_path[0])
        return path[-1][1]

    def _find(self, node: Node, request: str, weight: int = None) -> List[Tuple[int, Node]]:
        """
        TODO FIXME
        Возвращает узел, если поиск успешен
        Возвращает все не отверженные пути, если поиск не успешен и взвешивает их
        :param node:
        :param request:
        :return:
        """

        weight = weight or 0

        if len(request) == 0:
            return [(0, node), ]

        if node.is_leaf:
            # ToDo Add request
            return [(len(request.split(' ')), node), ]

        node_weights: Tuple[Tuple[Node, dict]] = tuple((child, _get_difference_point(child, request))
                                                       for child in node.children)

        logging.debug(f"node_weights --> {node_weights}")

        nodes: Tuple[Tuple[Node, dict]] = sorted(node_weights,
                                                 key=lambda node_data: node_data[1]['distance'])

        logging.debug(f"nodes --> {nodes}")

        def _find_path(child: Node, intersection: str, weight_child: int) -> tuple:
            return child, \
                   self._find(child, _get_difference(request, intersection), weight + weight_child)

        current_paths = []
        for child, paths in (_find_path(node, data['word'], data['distance']) for node, data in nodes):
            for path_weight, path in paths:
                if len(path) != 1:
                    path.append(child)

                current_paths.append((path_weight, path))

        if any(pair[0] == 0 for pair in current_paths):
            current_paths = list(filter(lambda pair: pair[0] == 0, current_paths))

        return current_paths


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    with open("menu.json", "r", encoding="utf-8") as write_file:
        menu_dict = json.load(write_file)

    example_tree = Tree(menu_dict)
    print(example_tree.find("Зонтики"))
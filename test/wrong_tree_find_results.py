from tree import Tree
from node import Node


dict_level_1 = {node_name:'https://www.google.ru' for node_name in ['LhWDa', 'cHRLD', 'jyGSs', 'ycAlK']}
tree = Tree(dict.fromkeys(['root'], dict_level_1))
print(tree._find(tree.root, 'jzADD', 0))

import random
import string


def get_random_string() -> str:
    return ''.join(random.choices(string.ascii_letters, k=random.randint(2, 8)))


def get_random_level() -> int:
    return random.randint(2, 10)


def generate_random_key_dict() -> dict:
    return {get_random_string(): {} for _ in range(get_random_level())}

def recursion_dict(example_dict: dict, level: int = None, max_level: int = None):
    for keys, values in example_dict.items():
        values

# ToDo

# 1. Генерировать произвольное дерево
# 2. Уметь обходить дерево рандомно сохраняя data -> делаешь из этого request (можно перемешать)
# 3. Путь из предыдущего пункта - передаешь функции find и сравниваешь результат
# 4*. Берешь несколько путей (как в пункте 2), произвольном порядке их смешиваешь и передаешь функции find

if __name__ == '__main__':
    tree = {"root": {}}
    level = tree['root']
    random_level = get_random_level()
    for num in range(random_level):
        recursion_dict(tree, num, random_level)

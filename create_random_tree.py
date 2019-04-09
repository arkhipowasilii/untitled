import random
import string


def get_random_string() -> str:
    return ''.join(random.choices(string.ascii_letters, k=random.randint(2, 8)))


def get_random_level() -> int:
    return random.randint(2, 10)


def generate_random_key_dict() -> dict:
    return {get_random_string(): {} for _ in range(get_random_level())}


def recursion_dict(root_dict: dict, level: int = None, max_level: int = None):
    if len(root_dict) == 0:
        root_dict = generate_random_key_dict()

    for key, value in root_dict.items():
        if level == max_level:
            root_dict[key] = get_random_string()
        else:
            root_dict[key] = recursion_dict(value, (level + 1), max_level)

    return root_dict


def get_random_dict(max_level):
    tree = {"root": {}}
    return recursion_dict(tree, 0, max_level-1)

# ToDo

# 1. Генерировать произвольное дерево
# 2. Уметь обходить дерево рандомно сохраняя data -> делаешь из этого request (можно перемешать)
# 3. Путь из предыдущего пункта - передаешь функции find и сравниваешь результат
# 4*. Берешь несколько путей (как в пункте 2), произвольном порядке их смешиваешь и передаешь функции find


if __name__ == '__main__':
    print(get_random_dict(10))


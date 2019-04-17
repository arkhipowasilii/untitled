import pytest

from create_random_tree import get_random_string
from str_service import get_distance


def test_distance_rnd():
    current_file = open("str_service_tests.py", "a")
    current_file.write("\n")

    count = 100000
    while count != 0:
        count -= 1

        word1, word2 = get_random_string(), get_random_string()
        distance = get_distance(word1, word2)

        # ToDo Rnd test
        # Add assert with intersect of `set(word)`
        # Нет четких условий, есть только граничные

        intersection = set(word1).intersection(word2)

        try:
            assert abs(len(word1)-len(word2)) <= distance, f"{word1} : {word2} -> {get_distance}"
            assert len(intersection) <= distance
            # assert
            # assert
        except AssertionError as error:
            current_file.write(f"assert get_distance('{word1}', '{word2}') == \n")
            # ToDo auto generate test with word1 and word2 and append it in this file auto

        # assert True, f"{word1} : {word2} -> {get_distance}"


def test_distance_few_len():
    pass
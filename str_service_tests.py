import pytest

from create_random_tree import get_random_string
from str_service import get_distance


def test_distance_rnd():
    count = 10000

    while count != 0:
        count -= 1

        word1, word2 = get_random_string(), get_random_string()
        distance = get_distance(word1, word2)

        # ToDo Rnd test
        # Add assert with intersect of `set(word)`
        # Нет четких условий, есть только граничные

        intersection_len = len(set(word1).intersection(word2))

        try:
            assert abs(len(word1)-len(word2)) < distance, f"{word1} : {word2} -> {get_distance}"
            # assert
            # assert
            # assert
        except AssertionError as error:
            # ToDo auto generate test with word1 and word2 and append it in this file auto
            raise error

        # assert True, f"{word1} : {word2} -> {get_distance}"


    pass


def test_distance_few_len():
    pass

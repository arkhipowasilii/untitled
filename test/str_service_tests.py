from create_random_tree import get_random_string
from str_service import get_distance

import logging

def test_distance_rnd():
    examples = list()
    count = 1000000
    while count != 0:
        count -= 1

        if count % 1000:
            logging.info(f"{count}")

        word1, word2 = get_random_string(), get_random_string()
        distance = get_distance(word1, word2)

        if word2 > word1:
            word1, word2 = word2, word1

        # ToDo Can change set to multiset from third lib
        intersection = list(set(word1).intersection(word2))

        # Mad not optimal
        additional = list()
        for char in intersection:
            char_count = min(len(tuple(None for chr in word1 if chr == char)),
                             len(tuple(None for chr in word2 if chr == char)))

            if char_count != 1:
                additional += [char] * (char_count - 1)

        intersection += additional
        # end mad

        try:
            assert abs(len(word1) - len(word2)) <= distance, \
                                        f"{word1} : {word2} -> {get_distance}"

            assert len(word1) - len(intersection) <= distance, \
                                        f"Intersection error: distance = {distance} {word1} ^ {word2} = {intersection}"

        except AssertionError as error:
            examples.append((word1, word2))
            logging.error(error)

    if len(examples) == 0:
        return

    with open("str_service_tests.py", "a") as current_file:
        current_file.write("\n")

        logging.error(f"Append tests for examples with len = {len(examples)}")
        for word1, word2 in examples:
            current_file.write(f"   assert get_distance('{word1}', '{word2}') == {input(f'{word1} - {word2} = ')}\n")


if __name__ == '__main__':
    test_distance_rnd()

def test_distance_few_len():
    assert get_distance('mGV', 'xGV') == 1
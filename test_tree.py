from tree import distance
import pytest


def tes_distance():
    assert distance("abc", '') == 3
    assert distance("abc", "xabcq") == 2
    assert distance("qwerty", "qaerty") == 1
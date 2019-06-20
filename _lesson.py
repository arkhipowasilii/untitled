from typing import List


class BigUInt:
    def __init__(self, number: str):
        self.numbers: List[int] = []
        for num in number:
            assert num.isdecimal()
            self.numbers.append(int(num))

    def __str__(self):
        return ''.join(tuple(map(str, self.numbers)))

    @classmethod
    def _create(cls, numbers: List[int]):
        assert all(num < 10 for num in numbers)

        result = cls('')
        result.numbers = list(numbers)
        return result

    def __gt__(self, other):
        left = self.numbers
        right = other.numbers

        if len(self.numbers) > len(other.numbers):
            return True
        elif len(self.numbers) < len(other.numbers):
            return False

        for index, num_self in enumerate(left):
            if num_self > right[index]:
                return True
            elif num_self < right[index]:
                return False
        return False

    def __lt__(self, other):
        return other.__gt__(self)

    def __add__(self, other: 'BigUInt'):

        left = self.numbers[::-1]
        right = other.numbers[::-1]

        if other > self:
            left, right = right, left

        result = left
        if left[len(right)-1] + right[-1] >= 10:
            result.append(0)

        for index, num_right in enumerate(right):

            if result[index] == 10:
                result[index] = 0
                result[index + 1] += 1

            current_num = result[index] + num_right

            if current_num < 10:
                result[index] = current_num
            else:
                result[index+1] += 1
                result[index] = current_num - 10


        print(result)
        return BigUInt._create(result[::-1])

    def __sub__(self, other):
        right = other.numbers[::-1]
        result = self.numbers[::-1]

        for index, num_right in enumerate(right):
            current_num = result[index] - num_right

            if current_num >= 0:
                result[index] = current_num
            else:
                result[index+1] = result[index+1]-1
                result[index] = 10 + current_num

        while result[-1] == 0:
            del result[-1]
        return BigUInt._create(result[::-1])


def bar(arg1, arg2, arg3):
    return arg1 + arg2


if __name__ == '__main__':
    a, b, c = BigUInt("99999"), BigUInt("4"), BigUInt("100")

    print(bar(a, b, c))

class BigUInt:
    def __init__(self, number: str):
        self.numbers = []
        for num in number:
            assert num.isdecimal()
            self.numbers.append(int(num))

    def __lt__(self, other):
        # ToDo Homework
        raise NotImplementedError()

    def __gt__(self, other):
        # ToDo homework
        raise NotImplementedError()

    def __add__(self, other):
        # ToDo Homework
        raise NotImplementedError()

    def __sub__(self, other):
        # ToDo Homework
        raise NotImplementedError()


def bar(arg1, arg2, arg3):
    return min(arg1, arg2) + arg3


if __name__ == '__main__':
    a, b, c = BigUInt("1"), BigUInt("10"), BigUInt("100")

    print(bar(a, b, c))

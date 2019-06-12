class BigUInt:
    def __init__(self, number: str = None, all_numbers: list = None):
        if all_numbers is not None:
            self.numbers = all_numbers
            number = ''
            for num in all_numbers:
                number += str(num)
                self.number = number[::-1]

        else:
            self.number = number
            self.numbers = []
            for num in number[::-1]:
                assert num.isdecimal()
                self.numbers.append(int(num))

    def __lt__(self, other):
        # ToDo Homework
        raise NotImplementedError()

    def __gt__(self, other):
        # ToDo homework
        raise NotImplementedError()

    def __add__(self, other):
        len_self = len(self.numbers)
        len_other = len(other.numbers)
        if len_other > len_self:
            self.numbers, other.numbers = other.numbers, self.numbers
            len_self, len_other = len_other, len_self

        result_numbers = [0 for _ in range(len_self+1)]

        for index in range(len_self):
            num_self = self.numbers[index]
            current_res_num = result_numbers[index]
            if index < len_other:
                num_other = other.numbers[index]
                current_num = num_self + num_other + current_res_num
                if current_num >= 10:
                    result_numbers[index] = current_num - 10
                    result_numbers[index+1] += 1
                else:
                    result_numbers[index] = current_num

            else:
                current_num = current_res_num + num_self
                if current_num == 10:
                    result_numbers[index+1] = 1
                    result_numbers[index] = 0
                else:
                    result_numbers[index] = current_num

        if result_numbers[-1] == 0:
            del result_numbers[-1]
        return BigUInt(all_numbers=result_numbers)

    def __sub__(self, other):
        len_self = len(self.numbers)
        len_other = len(other.numbers)

        result_numbers = [0 for _ in range(len_self+1)]

        for index in range(len_self):
            num_self = self.numbers[index]
            num_other = other.numbers[index]
            current_num = num_self - num_other + result_numbers[index]
            result_numbers[index+1] = -1
            if current_num >= 0:
                result_numbers[index] = current_num
            else:
                result_numbers[index] = 10 + current_num
                result_numbers[index+1] = -1

        return BigUInt(all_numbers=result_numbers)
def bar(arg1, arg2, arg3):
    return arg1 - arg2


if __name__ == '__main__':
    a, b, c = BigUInt("103"), BigUInt("101"), BigUInt("100")

    print(bar(a, b, c).number)

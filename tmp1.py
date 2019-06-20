class Foo:
    def __init__(self, data):
        self.d = data

    @classmethod
    def create(cls, data):
        return cls(data)

    @classmethod
    def create_or_raise(cls, data):
        assert data is not None
        return cls.create(data)

    def method(self):
        pass

class Bar(Foo):
    def __init__(self, data1, data2):
        super(Bar, self).__init__(data1)
        self.d2 = data2

    @classmethod
    def create(cls, data):
        return cls(None, data)


if __name__ == '__main__':
    Bar.create_or_raise(None)

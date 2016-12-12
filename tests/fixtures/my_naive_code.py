from unittest.mock import MagicMock

from overrides import overrides


def noop_decorator(func):
    return func


class MyNaiveOverride(MagicMock):
    def assert_any_call(self, *args, **kwargs):
        """
        Overrides without any marker.
        """
        print('Naive override')

    @noop_decorator
    def assert_called_with(self, *args, **kwargs):
        """
        Overrides without any marker.
        """
        print('Naive override')

    def new_method(self):
        pass

    @noop_decorator
    def anoter_method(self):
        pass


class MyCoscienteOverride(MagicMock):
    @overrides
    def assert_any_call(self, *args, **kwargs):
        """
        This one should not show any error since I marked it as a save
        override.
        """
        print('consciente override!')

    def new_method(self):
        pass

    @noop_decorator
    def anoter_method(self):
        pass


def main():
    naive = MyNaiveOverride()
    naive.assert_any_call()

    cosciente = MyCoscienteOverride()
    cosciente.assert_any_call()


if __name__ == '__main__':
    main()

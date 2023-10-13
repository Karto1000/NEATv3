# -----------------------------------------------------------
# Copyright (c) YPSOMED AG, Burgdorf / Switzerland
# YDS INNOVATION - Digital Innovation
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# email diginno@ypsomed.com
# author: Tim Leuenberger (Tim.leuenberger@ypsomed.com)
# -----------------------------------------------------------
import math
import typing

T = typing.TypeVar('T')


class IdentificationCollection(typing.Generic[T]):
    def __init__(self, sort_key: typing.Callable = None):
        self.__list: list[T] = []
        self.__dict: dict[float, T] = {}
        self.__sort_key = sort_key

    @typing.overload
    def get(self, index: int) -> typing.Optional[T]:
        ...

    @typing.overload
    def get(self, identification_number: float) -> typing.Optional[T]:
        ...

    def index(self, object_to_get: T) -> int:
        return self.__dict.get(object_to_get.__hash__())

    def get(self, param):
        if isinstance(param, int):
            try:
                return self.__list[param]
            except IndexError:
                return None

        if isinstance(param, float):
            return self.__dict.get(param)

    @typing.overload
    def remove(self, object_to_remove: T) -> bool:
        ...

    @typing.overload
    def remove(self, identification_number: float) -> bool:
        ...

    def remove(self, param):
        if isinstance(param, float):
            object_ = self.__dict.get(param)

            if not object_:
                return False

            del self.__dict[param]
            self.__list.remove(object_)

            return True

        if not self.__dict.get(param.__hash__()):
            return False

        del self.__dict[param.__hash__()]
        self.__list.remove(param)
        return True

    def add(self, object_to_add: T):
        self.__list.append(object_to_add)
        self.__dict[object_to_add.__hash__()] = object_to_add
        if self.__sort_key:
            self.__list.sort(key=self.__sort_key)

    def contains(self, object_: T) -> bool:
        return not not self.__dict.get(object_.__hash__())

    def clear(self):
        self.__list.clear()
        self.__dict.clear()

    def size(self) -> int:
        return len(self.__list)

    def __iter__(self):
        return self.__list.__iter__()

    def __next__(self):
        return next(self)

    def __len__(self):
        return self.__list.__len__()

    def __getitem__(self, item):
        if len(self.__list) == 0:
            raise IndexError("Cannot get element from empty list")

        return self.__list.__getitem__(item)

    def __repr__(self):
        return self.__list.__repr__()

    def items(self) -> list[T]:
        return self.__list


def sigmoid(x):
    return 1 / (1 + math.exp(-x))

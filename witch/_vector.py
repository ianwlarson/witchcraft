#!/usr/bin/env python3

import array
import copy

def sint(val):
    return val.__sint__()


class WVec:

    @property
    def core(self):
        return self._core

    @classmethod
    def ones(cls, length):
        return cls([1] * length)

    @classmethod
    def zeros(cls, length):
        return cls([0] * length)

    def __init__(self, i_val, length=None, signed=False):

        self.signed = signed

        if isinstance(i_val, self.__class__):
            self._core = copy.copy(i_val.core)
        elif type(i_val) is str:
            for c in i_val:
                if c not in ['0', '1']:
                    raise ValueError('Invalid string literal, cannot construct WVec instance.')

            self._core = array.array('B', [int(c) for c in i_val])
            self._core.reverse()
        elif type(i_val) is int:
            if i_val < 0:
                raise NotImplementedError()
            else:
                self._core = array.array('B', [int(c) for c in bin(i_val)[2:]])
                self._core.reverse()
        elif type(i_val) is list:
            for elem in i_val:
                if elem not in [0, 1, '1', '0']:
                    raise ValueError('Invalid element in list, cannot construct WVec instance.')

            self._core = array.array('B', map(int, i_val))
        else:
            raise ValueError("Cannot construct WVec from {}".format(type(i_val)))

        if length is not None:
            if length < len(self):
                raise ValueError("Supplied length cannot contain assigned value.")

            length -= len(self)
            if self.signed and self._core[-1] is 1:
                raise NotImplementedError()
                self._core.extend([1 for i in range(length)])
            else:
                self._core.extend([0 for i in range(length)])

    def __getitem__(self, item):
        return self._core[item]

    def __setitem__(self, key, value):

        if type(value) is str:
            if value not in ['1', '0']:
                raise ValueError()
            else:
                self._core[key] = int(value)
        elif type(value) is int:
            if value not in [1, 0]:
                raise ValueError()
            else:
                self._core[key] = value
        elif type(value) is bool:
            self._core[key] = int(value)
        else:
            raise ValueError()

    def __eq__(self, other):

        if isinstance(other, self.__class__):
            return self._core == other._core
        elif type(other) is str:
            return self == WVec(other, length=len(self))
        elif type(other) is int:
            if other < 0:
                # TODO What should I do here?
                raise NotImplementedError()
            else:
                return self == WVec(other, length=len(self))
        elif type(other) is list:
            return self == WVec(other, length=len(self))
        else:
            raise ValueError("Cannot compare.")

    def __len__(self):

        return len(self._core)

    def __str__(self):
        tmp = list(map(str, self._core))
        tmp.reverse()

        return "".join(tmp)

    def __add__(self, other):

        if len(other) > len(self):
            a = self.__class__(self, length=len(other))
            b = self.__class__(other)
            out = self.__class__(0, length=len(other))
        else:
            a = self.__class__(other, length=len(self))
            b = self.__class__(self)
            out = self.__class__(0, length=len(self))

        carry = 0
        for i in range(len(out)):
            out[i] = a[i] ^ b[i] ^ carry
            carry = (a[i] & b[i]) | (carry & (a[i] ^ b[i]))

        if carry is 1:
            out._core.append(1)

        return out

    def __sub__(self, other):
        # 100 - 001 = 011

        raise NotImplementedError()

    def __xor__(self, other):

        if type(other) in [int, str, list]:
            other = self.__class__(other)

        if len(other) > len(self):
            out = WVec(self, length=len(other))
            for i in range(len(other)):
                out[i] = out[i] ^ other[i]
        else:
            out = WVec(other, length=len(self))
            for i in range(len(self)):
                out[i] = out[i] ^ self[i]

        return out

    def __lshift__(self, other):
        raise NotImplementedError()

    def __and__(self, other):

        if type(other) in [int, str, list]:
            other = self.__class__(other)

        if len(other) > len(self):
            out = WVec(self, length=len(other))
            for i in range(len(other)):
                out[i] &= other[i]
        else:
            out = WVec(other, length=len(self))
            for i in range(len(self)):
                out[i] &= self[i]

        return out

    def __or__(self, other):

        if type(other) in [int, str, list]:
            other = self.__class__(other)

        if len(other) > len(self):
            out = WVec(self, length=len(other))
            for i in range(len(other)):
                out[i] |= other[i]
        else:
            out = WVec(other, length=len(self))
            for i in range(len(self)):
                out[i] |= self[i]

        return out

    def __invert__(self):

        out = WVec(0, length=len(self))

        for i in range(len(out)):
            out[i] = int(not self[i])

        return out

# End of file

import abc
import re
from enum import Enum, unique
from typing import List

from define.const import *


@unique
class Token(Enum):
    CONDITION = 1
    ACTION = 2
    EXCEPT_RESULT = 3
    LOCATION = 4
    INVALID = 5
    STATUS = 6


class TokenStream:
    __slots__ = ["_token", "_key_word", "_span"]

    def __init__(self, token: Token, kw: str, span: str):
        self._token = token
        self._key_word = kw
        self._span = span

    def token(self) -> Token:
        return self._token

    def span(self) -> str:
        return self._span

    def keyword(self) -> str:
        return self._key_word

    def __str__(self):
        return f"token:{self._token},kw: `{self._key_word}`, value:{self._span}"

    def __repr__(self):
        return f"token:{self._token}, kw: `{self._key_word}`, value:{self._span}"


class BasicScanner(metaclass=abc.ABCMeta):
    __slots__ = []

    @abc.abstractmethod
    def next(self, line: str) -> List[TokenStream]:
        pass


class LineScanner(BasicScanner):

    def __init__(self):
        self._re = re.compile(r"(?P<expr>\w+?)<(?P<expr_v>.+?)>")
        self._recursive_re = re.compile(r"(?P<expr>\w+?)<(?P<expr_v>.+)>")

    def next(self, line: str) -> List[TokenStream]:
        return [t for t in map(self.to_token, self._re.finditer(line))]

    def to_token(self, k: dict) -> TokenStream:
        key = k[KW_KEY]
        value = k[KW_VALUE]
        token = self.kind(key)
        if token == Token.INVALID:
            raise InvalidToken(f"{key}<{value}> invalid keyword: {key}")
        return TokenStream(token, key, value)

    @staticmethod
    def kind(k) -> Token:
        if k in STATUS_KW_LIST:
            return Token.STATUS
        elif k in ACTION_KW_LIST:
            return Token.ACTION
        elif k in CONDITION_KW_LIST:
            return Token.CONDITION
        elif k in LOCATION_KW_LIST:
            return Token.LOCATION
        elif k in EXCEPT_KW_LIST:
            return Token.EXCEPT_RESULT
        else:
            return Token.INVALID


class InvalidToken(Exception):
    pass

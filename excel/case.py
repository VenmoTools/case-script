import abc
import re
from typing import Tuple

from define.constsentences import StepSentences, ConditionSentences, DescriptionSentences, StatusSentences, \
    LocationSentences
from lexer.ast import AST, ASTNode
from lexer.parser import Token

CLASSNAME_RE = re.compile(r"'.+?\.(.+?)'")


class Column:
    NO = (0, "用例编号")
    NAME = (1, "用例名称")
    DESCRIPTION = (2, "用例描述")
    MODULE = (3, "所属模块")
    CONDITION = (4, "前置条件")
    STEP = (5, "操作步骤")
    EXCEPT = (6, "预期结果")
    ACTUAL = (7, "实际结果")
    STATUS = (8, "状态")
    EXE_TIME = (9, "测试时间")
    TESTER = (10, "执行人员")
    NOTE = (11, "备注")


MAPPING = {value[0]: name.lower() for name, value in Column.__dict__.items() if "__" not in name}
CASE_ID_FORMAT = "CA_TEST_{}"


class Cell:
    __slots__ = ["col", "row"]

    def __init__(self, col=0, row=0):
        self.col = col
        self.row = row

    def position(self) -> Tuple[int, int]:
        return self.row, self.col

    def content(self) -> str:
        pass

    def set_row(self, row):
        self.row = row
        return self

    def set_col(self, col):
        self.col = col
        return self

    def cell_type(self) -> Tuple[int, str]:
        pass


class CaseSerializer(metaclass=abc.ABCMeta):
    __slots__ = []

    @abc.abstractmethod
    def serialize(self) -> str:
        pass

    @abc.abstractmethod
    def deserialize(self, node: ASTNode):
        pass

    @abc.abstractmethod
    def args_parser(self, line: str):
        pass


class ClassInfo(metaclass=abc.ABCMeta):
    """
    the __str__ must return class name
    """

    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass


class CaseNo(Cell, ClassInfo):
    def __str__(self):
        return "class_no"

    def __repr__(self):
        return "class_no"

    __slots__ = ["col", "row", "_no"]

    def __init__(self, row, fmt=CASE_ID_FORMAT):
        super().__init__(Column.NO[0], row)
        self._no = fmt.format(row)

    def content(self):
        return self._no

    def cell_type(self) -> Tuple[int, str]:
        return Column.NO


class CaseName(Cell, CaseSerializer):
    __slots__ = ["col", "row", "_name"]

    def __init__(self, name: str):
        super().__init__(Column.NAME[0])
        self._name = name

    def serialize(self) -> str:
        return self._name

    def deserialize(self, node: str):
        pass

    def content(self) -> str:
        return self.serialize()

    def cell_type(self) -> Tuple[int, str]:
        return Column.NAME

    def args_parser(self, line: str):
        pass


class CaseDescription(Cell, CaseSerializer):
    __slots__ = ["col", "row", "_desc"]

    def __init__(self, desc):
        super().__init__(Column.DESCRIPTION[0])
        self._desc = desc

    def serialize(self) -> str:
        return self._desc

    def deserialize(self, node: str):
        pass

    def content(self) -> str:
        return self.serialize()

    def cell_type(self) -> Tuple[int, str]:
        return Column.DESCRIPTION

    def args_parser(self, line: str):
        pass


class FrontCondition(Cell, CaseSerializer):
    __slots__ = ["col", "row", "_name", "_no"]

    def __init__(self):
        super().__init__(Column.CONDITION[0])
        self._name = []
        self._no = 1

    def deserialize(self, node: AST):
        if node.tk != Token.CONDITION:
            raise TypeError(f"except condition token given {node.tk}")

        status = 0x00
        # need Optimized
        for n in node:
            token = n.token.token()
            kw = n.token.keyword()
            if token == Token.CONDITION:
                if kw == "at":
                    status <<= 4
                else:
                    status <<= 1
            if token == Token.STATUS:
                status <<= 2
            if token == Token.LOCATION:
                status <<= 3

        n = next(node)
        kw = n.token.keyword()
        # 0b11 => one kw
        if status == 0x01:
            if kw == "value_is":
                return ConditionSentences.value_is(*self.args_parser(n.span()))
            elif kw == "content_is":
                return ConditionSentences.content_is(*self.args_parser(n.span()))
            if kw in ["n_exists", "exists"]:
                no = True if kw == "exists" else False
                content, item, number = self.args_parser(n.span())
                return ConditionSentences.exists_or_not(number, item, content, not_exists=no)
        # status
        if status == 0x03:
            if kw == "request":
                return ConditionSentences.request_status(n.span(), self.const(next(node).span()))
            elif kw == "n_request":
                return ConditionSentences.request_not_status(n.span(), self.const(next(node).span()))
        if status == 0b111:
            no = True if kw == "exists" else False
            content, item, number = self.args_parser(n.span())
            return ConditionSentences.exists_in_somewhere_or_not(SentencesMaker.make_location(next(node)), number, item,
                                                                 content,
                                                                 not_exists=no)
        if status == 0x1111:
            no = True if kw == "exists" else False
            content, item, number = self.args_parser(n.span())
            locat = SentencesMaker.make_location(next(node))
            pass
        self._no += 1

    def serialize(self) -> str:
        return ";\n".join([str(step) for step in self._name])

    def content(self) -> str:
        return self.serialize()

    def cell_type(self) -> Tuple[int, str]:
        return Column.CONDITION

    def args_parser(self, line: str):
        if "," in line:
            return (self.const(x.replace(" ", "")) for x in line.split(","))

    @staticmethod
    def const(x):
        if "unit" in x:
            return DescriptionSentences.__dict__[x.split("::")[1].upper()]
        if "status" in x:
            return StatusSentences.__dict__[x.split("::")[1].upper()]
        if "number" in x:
            return re.findall(r"[\w]\(([\d])\)", x)[0]
        return x


class EmptyCell(Cell):
    __slots__ = []

    def content(self) -> str:
        return ""


class FunctionModule(Cell, CaseSerializer):
    __slots__ = ["col", "row", "_name"]

    def __init__(self, name):
        super().__init__(Column.MODULE[0])
        self._name = name

    def deserialize(self, node: ASTNode):
        pass

    def serialize(self) -> str:
        return self._name

    def content(self) -> str:
        return self.serialize()

    def cell_type(self) -> Tuple[int, str]:
        return Column.MODULE


class StepDescription(Cell, CaseSerializer):
    __slots__ = ["col", "row", "_steps"]

    def __init__(self):
        super().__init__(Column.STEP[0])
        self._steps = []

    def add_step(self, step: StepSentences):
        self._steps.append(step)
        return self

    def deserialize(self, node: str):
        pass

    def serialize(self) -> str:
        return ";\n".join([str(step) for step in self._steps])

    def content(self) -> str:
        return self.serialize()

    def cell_type(self) -> Tuple[int, str]:
        return Column.STEP


class ActualResult(Cell):

    def __init__(self):
        super().__init__(Column.ACTUAL[0])

    def content(self) -> str:
        return ""

    def cell_type(self) -> Tuple[int, str]:
        return Column.ACTUAL


class ExceptResult(Cell, CaseSerializer):
    __slots__ = ["col", "row", "_steps"]

    def __init__(self, ):
        super().__init__(Column.EXCEPT[0])
        self._steps = []

    def add_step(self, step: StepSentences):
        self._steps.append(step)
        return self

    def serialize(self) -> str:
        return ";\n".join([str(step) for step in self._steps])

    def deserialize(self, node: str):
        pass

    def content(self) -> str:
        return self.serialize()

    def cell_type(self) -> Tuple[int, str]:
        return Column.EXCEPT


class Note(Cell, CaseSerializer):
    __slots__ = ["col", "row"]

    def __init__(self):
        super().__init__(Column.NOTE[0])

    def serialize(self) -> str:
        return "无"

    def deserialize(self, node: str):
        pass

    def content(self) -> str:
        return self.serialize()

    def cell_type(self) -> Tuple[int, str]:
        return Column.NOTE


class TestCase:
    def __init__(self, no):
        assert no >= 1, "row number must great than 1"
        self.__no = no
        self.no = CaseNo(no)

    def set(self, col: Tuple[int, str], value):
        assert isinstance(value, Cell), "set invalid value to TestCase"
        if isinstance(value, CaseNo):
            return
        index, name = col
        attr = MAPPING[index]
        if isinstance(value, EmptyCell):
            value.set_col(index)
        value.set_row(self.__no)
        setattr(self, attr, value)
        return self

    def to_list(self):
        name = filter(lambda x: "TestCase" not in x, [key for key in self.__dict__])
        attrs = [value for key, value in self.__dict__.items() if "TestCase" not in key]
        assert len(attrs) == len(MAPPING), "no enough case element"
        empty_cell = str(EmptyCell().__class__)
        for n, c in zip(name, attrs):
            c_name = CLASSNAME_RE.findall(str(c.__class__))[0]
            if c_name in empty_cell:
                continue
            assert n in c_name.lower(), f"missing {n} filed"
        attrs.sort(key=lambda x: x.col)
        return attrs


class EmptyCaseElement(Exception):
    pass


class SentencesMaker:
    def __init__(self, no):
        self.case = TestCase(no)

    def make(self) -> str:
        pass

    @staticmethod
    def get_attr(o, a):
        if hasattr(o, a):
            return getattr(o, a)
        raise TypeError(f"can not find attr `{a}`")

    @staticmethod
    def _make_location_attr(kw: str):
        other = "somewhere"
        if "parti" in kw:
            other = "particular_somewhere"
        return f"{kw}_{other}"

    @classmethod
    def make_condition(cls, node: ASTNode):
        pass

    @classmethod
    def make_location(cls, node: ASTNode):
        kw = node.token.keyword()
        sentences = LocationSentences()
        try:
            attr = cls._make_location_attr(kw)
            func = cls.get_attr(sentences, attr)
            if "parti" in kw:
                return func(*cls.args_parser(node.token.span()))
            return func(node.token.token())
        except KeyError:
            if kw == "location":
                return cls.get_attr(sentences, node.token.span())()
            else:
                raise SyntaxError(f"can not find keyword `{kw}`")

    @classmethod
    def args_parser(cls, line: str):
        if "," in line:
            return (cls.const(x.replace(" ", "")) for x in line.split(","))

    @classmethod
    def const(cls, x):
        if "unit" in x:
            if "cust" in x:
                return re.findall(r"\(.+?\)", x)[0]
            return DescriptionSentences.__dict__[x.split("::")[1].upper()]
        if "status" in x:
            return StatusSentences.__dict__[x.split("::")[1].upper()]
        if "number" in x:
            return re.findall(r"[\w]\(([\d])\)", x)[0]
        if "location" in x:
            return x.split("::")[1]

        return x


if __name__ == '__main__':
    s = LocationSentences()
    print(hasattr(s, "right"))

from typing import Tuple, List


class Sentences:
    # CLICK
    CLICK_NAME = "点击【{name}】按钮"
    CLICK_WITH_LOCATION = "在{location}点击【{name}】按钮"
    CLICK_WITH_SOMETHING = "点击【{some_thing}】的【{name}】按钮"
    # INPUT
    INPUT_NAME = "在【{name}】输入框输入【{value}】"
    INPUT_WITH_LOCATION_OR_SOMETHING = "在{location}的【{name}】输入框中输入【{value}】"
    # DRAG
    DRAG_SOMETHING = "将【{name}】拖动至【{some_where}】"
    DRAG_PARTICULAR_SOMETHING_TO_SOMEWHERE = "将{from_location}的【{name}】拖动至【{some_where}】处"
    DRAG_PARTICULAR_SOMETHING_TO_PARTICULAR_SOMEWHERE = "将{from_location}的【{name}】拖动至{to_location}的【{some_where}】处"
    DRAG_SOMETHING_TO_PARTICULAR_SOMEWHERE = "将【{name}】拖动至【{to_location}】的【{some_where}】处"
    # OPEN
    OPEN_NAME = "打开【{name}】"
    OPEN_SOMEWHERE = "打开{location}的【{name}】"
    OPEN_SITUATION = "{situation}打开【{name}】"
    # SELECT
    SELECT_NAME = "选择【{name}】"
    SELECT_NAME_WITH_DESC = "选择【{name}】【{description}】"
    SELECT_SOMEWHERE = "选择{location}的【{name}】"
    SELECT_SOMEWHERE_WITH_DESC = "选择{location}的【{name}】【{description}】"
    SELECT_PARTICULAR_SOMETHING = "在{location}选择【{name}】"
    # OTHER
    FORWARD = "前往至【{some_where}】"
    BACK_TO = "后退至【{some_where}】"
    RETURN_TO = "返回【{some_where}】"
    JUMP_TO = "跳转到【{some_where}】"
    REPEAT_STEP = "重复第【{no}】步骤"
    FIND_THEN_DO = "找到【{name}】并【{action}】"
    # LOCATION
    IN_SOMEWHERE = "【{some_where}】中"
    IN_PARTICULAR_SOMEWHERE = "【{particular}】中的【{some_where}】处"
    LEFT_SOMEWHERE = "【{some_where}】左侧"
    LEFT_PARTICULAR_SOMEWHERE = "【{particular}】左侧的【{some_where}】处"
    RIGHT_SOMEWHERE = "【{some_where}】右侧"
    RIGHT_PARTICULAR_SOMEWHERE = "【{particular}】右侧的【{some_where}】处"
    ABOVE_SOMEWHERE = "【{some_where}】上方"
    ABOVE_PARTICULAR_SOMEWHERE = "【{particular}】上方的【{some_where}】处"
    BOTTOM_SOMEWHERE = "【{some_where}】下方"
    BOTTOM_PARTICULAR_SOMEWHERE = "【{particular}】下方的【{some_where}】处"
    BOTTOM_RIGHT = "【右下角】"
    BOTTOM_LEFT = "【左下角】"
    TOP_RIGHT = "【右上角】"
    TOP_LEFT = "【左上角】"
    TOP = "【最上方】"
    BOTTOM = "【最下方】"
    MIDDLE = "【中间】"
    LEFT = "【左侧】"
    RIGHT = "【右侧】"
    # except
    EXCEPT_DISPLAY = "【{something}】回显正常"
    EXCEPT_SOMEWHERE_DISPLAY = "{location}的【{something}】回显正常"
    EXCEPT_PARTICULAR_SOMEWHERE_DISPLAY = "{location}的【{some_where}】为【{something}】"
    EXCEPT_RESULT_IS = "【{something}】结果为【{name}】"
    EXCEPT_STATUS = "【{something}】处于【{status}】状态"
    EXCEPT_SHOW_SOMETHING = "{location}弹出 / 出现【{something}】"
    EXCEPT_SHOW_SOMETHING_IN_SOMEWHERE = "在{location}显示【{something}】"
    EXCEPT_CHANGE = "【{something}】转变为【{other}】"
    EXCEPT_NOTE = "提示【{something}】"
    EXCEPT_NOTE_AT_SOMEWHERE = "在{location}提示【{something}】"
    EXCEPT_INCLUDE = "在【{somewhere}】包含【{something}】"
    EXCEPT_EXISTS = "在【{somewhere}】中存在【{something}】{description}"

    SITUATION = "当处于【{situation}】情况下,"
    SITUATION_STATUS = "当处于【{status}】状态时,"
    SITUATION_WHEN = "当处于【{when}】时,"

    CONDITION_REQUEST_STATUS = "【{something}】必须为【{status}】状态"
    CONDITION_REQUEST_NOT_STATUS = "【{something}】不能是【{status}】状态"
    CONDITION_AND = "，并且【{condition}】"
    CONDITION_OR = "，或者【{condition}】"
    CONDITION_VALUE_IS = "【{something}】的值为【{value}】"
    CONDITION_CONTENT_IS = "【{something}】的内容为【{content}】"
    CONDITION_IN_LIST = "【{something}】处下列于其中一项：【{lists}】"
    CONDITION_EXISTS = "{not_exists}存在【{number}{unit}{something}{description}】"
    CONDITION_EXISTS_IN_SOMEWHERE = "在{location}{not_exists}存在【{number}{unit}{something}{description}】"
    CONDITION_EXISTS_WITH_WHEN = "{when}" + CONDITION_EXISTS
    CONDITION_EXISTS_IN_SOMEWHERE_WITH_WHEN = "{when}" + CONDITION_EXISTS_IN_SOMEWHERE


class SituationSentences:
    @staticmethod
    def in_status(status: str) -> str:
        return Sentences.SITUATION_STATUS.format(status=status)

    @staticmethod
    def in_situation(situation: str) -> str:
        return Sentences.SITUATION.format(situation=situation)

    @staticmethod
    def when(when: str) -> str:
        return Sentences.SITUATION_WHEN.format(when=when)


class LocationSentences:
    __slots__ = ["_msg"]

    def __init__(self):
        self._msg = ""

    @property
    def msg(self) -> str:
        return self._msg

    @msg.setter
    def msg(self, msg):
        self._msg = msg

    @classmethod
    def in_somewhere(cls, some_where):
        f = cls()
        f.msg = Sentences.IN_SOMEWHERE.format(some_where=some_where)
        return f

    @classmethod
    def in_particular_somewhere(cls, particular, some_where):
        f = cls()
        f.msg = Sentences.IN_PARTICULAR_SOMEWHERE.format(particular=particular, some_where=some_where)
        return f

    @classmethod
    def left_somewhere(cls, some_where):
        f = cls()
        f.msg = Sentences.LEFT_SOMEWHERE.format(some_where=some_where)
        return f

    @classmethod
    def left_particular_somewhere(cls, particular, some_where):
        f = cls()
        f.msg = Sentences.LEFT_SOMEWHERE.format(particular=particular, some_where=some_where)
        return f

    @classmethod
    def right_somewhere(cls, some_where):
        f = cls()
        f.msg = Sentences.LEFT_SOMEWHERE.format(some_where=some_where)
        return f

    @classmethod
    def right_particular_somewhere(cls, particular, some_where):
        f = cls()
        f.msg = Sentences.LEFT_PARTICULAR_SOMEWHERE.format(particular=particular, some_where=some_where)
        return f

    @classmethod
    def above_somewhere(cls, some_where):
        f = cls()

        f.msg = Sentences.ABOVE_SOMEWHERE.format(some_where=some_where)
        return f

    @classmethod
    def above_particular_somewhere(cls, particular, some_where):
        f = cls()
        f.msg = Sentences.ABOVE_PARTICULAR_SOMEWHERE.format(particular=particular, some_where=some_where)
        return f

    @classmethod
    def bottom_somewhere(cls, some_where):
        f = cls()
        f.msg = Sentences.BOTTOM_SOMEWHERE.format(some_where=some_where)
        return f

    @classmethod
    def bottom_particular_somewhere(cls, particular, some_where):
        f = cls()
        f.msg = Sentences.BOTTOM_PARTICULAR_SOMEWHERE.format(particular=particular, some_where=some_where)
        return f

    @classmethod
    def bottom_right(cls):
        f = cls()
        f.msg = Sentences.BOTTOM_RIGHT
        return f

    @classmethod
    def bottom_left(cls):
        f = cls()
        f.msg = Sentences.BOTTOM_LEFT
        return f

    @classmethod
    def top_right(cls):
        f = cls()
        f.msg = Sentences.TOP_RIGHT
        return f

    @classmethod
    def top_left(cls):
        f = cls()
        f.msg = Sentences.TOP_LEFT
        return f

    @classmethod
    def top(cls):
        f = cls()
        f.msg = Sentences.TOP
        return f

    @classmethod
    def bottom(cls):
        f = cls()
        f.msg = Sentences.BOTTOM
        return f

    @classmethod
    def middle(cls):
        f = cls()
        f.msg = Sentences.MIDDLE
        return f

    @classmethod
    def left(cls):
        f = cls()
        f.msg = Sentences.LEFT
        return f

    @classmethod
    def right(cls):
        f = cls()
        f.msg = Sentences.RIGHT
        return f


class ActionSentences:

    @staticmethod
    def click_something(name: str) -> str:
        return Sentences.CLICK_NAME.format(name=name)

    @staticmethod
    def click_something_with_location(name: str, location: LocationSentences) -> str:
        return Sentences.CLICK_WITH_LOCATION.format(name=name, location=location.msg)

    @staticmethod
    def click_somethings_item(name: str, some_thing: str, ) -> str:
        return Sentences.CLICK_WITH_SOMETHING.format(name=name, some_thing=some_thing)

    @staticmethod
    def input_something(name: str, value: str, ) -> str:
        return Sentences.INPUT_NAME.format(name=name, value=value)

    @staticmethod
    def input_something_with_location(name: str, location: LocationSentences, value: str) -> str:
        return Sentences.INPUT_WITH_LOCATION_OR_SOMETHING.format(name=name, location=location.msg, value=value)

    @staticmethod
    def drag_something_to_somewhere(name: str, some_where: str) -> str:
        return Sentences.DRAG_SOMETHING.format(name=name, some_where=some_where)

    @staticmethod
    def drag_particular_something_to_somewhere(name: str, from_location: LocationSentences, some_where: str) -> str:
        return Sentences.DRAG_PARTICULAR_SOMETHING_TO_SOMEWHERE.format(name=name, from_location=from_location.msg,
                                                                       some_where=some_where)

    @staticmethod
    def drag_particular_something_to_particular_somewhere(name: str, from_location: LocationSentences,
                                                          to_location: LocationSentences,
                                                          some_where: str) -> str:
        return Sentences.DRAG_PARTICULAR_SOMETHING_TO_PARTICULAR_SOMEWHERE.format(name=name,
                                                                                  from_location=from_location.msg,
                                                                                  to_location=to_location.msg,
                                                                                  some_where=some_where)

    @staticmethod
    def drag_something_to_particular_somewhere(name: str, from_location: LocationSentences, some_where: str) -> str:
        return Sentences.DRAG_SOMETHING_TO_PARTICULAR_SOMEWHERE.format(name=name, from_location=from_location.msg,
                                                                       some_where=some_where)

    @staticmethod
    def select_name(name: str) -> str:
        return Sentences.SELECT_NAME.format(name=name)

    @staticmethod
    def select_name_with_desc(name: str, desc: str) -> str:
        return Sentences.SELECT_NAME_WITH_DESC.format(name=name, description=desc)

    @staticmethod
    def select_somewhere(name: str, location: LocationSentences) -> str:
        return Sentences.SELECT_SOMEWHERE.format(name=name, location=location.msg)

    @staticmethod
    def select_somewhere_with_desc(name: str, location: LocationSentences, desc: str) -> str:
        return Sentences.SELECT_SOMEWHERE_WITH_DESC.format(name=name, location=location.msg, description=desc)

    @staticmethod
    def select_particular_something(name: str, location: LocationSentences) -> str:
        return Sentences.SELECT_PARTICULAR_SOMETHING.format(name=name, location=location.msg)

    @staticmethod
    def open_name(name: str) -> str:
        return Sentences.OPEN_NAME.format(name=name)

    @staticmethod
    def open_somewhere(name: str, location: LocationSentences) -> str:
        return Sentences.OPEN_SOMEWHERE.format(name=name, location=location.msg)

    @staticmethod
    def open_situation(name: str, situation: str) -> str:
        return Sentences.OPEN_SITUATION.format(name=name, situation=situation)

    @staticmethod
    def forward(some_where: str) -> str:
        return Sentences.FORWARD.format(some_where=some_where)

    @staticmethod
    def back_to(some_where: str) -> str:
        return Sentences.BACK_TO.format(some_where=some_where)

    @staticmethod
    def jump_to(some_where: str) -> str:
        return Sentences.JUMP_TO.format(some_where=some_where)

    @staticmethod
    def return_to(some_where: str) -> str:
        return Sentences.RETURN_TO.format(some_where=some_where)

    @staticmethod
    def repeat_no_step(no: int) -> str:
        return Sentences.REPEAT_STEP.format(no=no)

    @staticmethod
    def find_then_do(name: str, action: str) -> str:
        return Sentences.REPEAT_STEP.format(name=name, action=action)


class StepSentences:
    __slots__ = ["_no", "_desc"]

    def __init__(self, no):
        self._no = no
        self._desc = ""

    def make(self, step: str):
        assert self._no > 0
        self._desc = step
        return self

    def __str__(self):
        return f"{self._no}. {self._desc}"

    def __repr__(self):
        return f"{self._no}. {self._desc}"


class StatusSentences:
    __slots__ = []

    ENABLE = "可用"
    DISABLE = "不可用"
    DELETE = "已删除"
    N_DELETE = "未删除"
    EXITS = "已存在"
    N_EXITS = "不存在"
    ACTIVE = "已激活"
    N_ACTIVE = "未激活"


class DescriptionSentences:
    ITEM = "项"
    NUMBER = "个"
    RECORD = "记录"
    NUMBER_OF = "条"


class ExceptSentences:

    @staticmethod
    def except_display_something(something: str) -> str:
        return Sentences.EXCEPT_DISPLAY.format(something=something)

    @staticmethod
    def except_location_display_something(something: str, location: LocationSentences) -> str:
        return Sentences.EXCEPT_SOMEWHERE_DISPLAY.format(something=something, location=location.msg)

    @staticmethod
    def except_display_particular_somewhere(something: str, location: LocationSentences, somewhere: str) -> str:
        return Sentences.EXCEPT_PARTICULAR_SOMEWHERE_DISPLAY.format(something=something, somewhere=somewhere,
                                                                    location=location.msg)

    @staticmethod
    def except_result_is(something: str, name: str) -> str:
        return Sentences.EXCEPT_RESULT_IS.format(something=something, name=name)

    @staticmethod
    def except_status(something: str, status: StatusSentences) -> str:
        return Sentences.EXCEPT_STATUS.format(something=something, status=status)

    @staticmethod
    def except_show_something_at(location: LocationSentences, something: str) -> str:
        return Sentences.EXCEPT_SHOW_SOMETHING.format(location=location.msg, something=something)

    @staticmethod
    def except_show_something_in(location: LocationSentences, something: str) -> str:
        return Sentences.EXCEPT_SHOW_SOMETHING_IN_SOMEWHERE.format(location=location.msg, something=something)

    @staticmethod
    def except_change_to(something: str, to_something: str) -> str:
        return Sentences.EXCEPT_CHANGE.format(something=something, to_something=to_something)

    @staticmethod
    def except_note(note: str) -> str:
        return Sentences.EXCEPT_NOTE.format(something=note)

    @staticmethod
    def except_note_at(location: LocationSentences, note: str) -> str:
        return Sentences.EXCEPT_NOTE_AT_SOMEWHERE.format(location=location.msg, something=note)

    @staticmethod
    def except_include(somewhere: str, something: str) -> str:
        return Sentences.EXCEPT_INCLUDE.format(somewhere=somewhere, something=something)

    @staticmethod
    def except_exists(somewhere: str, something: str, description: str) -> str:
        return Sentences.EXCEPT_EXISTS.format(somewhere=somewhere, something=something, description=description)


class ConditionSentences:

    @staticmethod
    def request_status(something: str, status: str) -> str:
        return Sentences.CONDITION_REQUEST_STATUS.format(something=something, status=status)

    @staticmethod
    def request_not_status(something: str, status: str) -> str:
        return Sentences.CONDITION_REQUEST_NOT_STATUS.format(something=something, status=status)

    @staticmethod
    def condition_and(other_condition: str):
        return Sentences.CONDITION_AND.format(condition=other_condition)

    @staticmethod
    def condition_or(other_condition: str):
        return Sentences.CONDITION_OR.format(condition=other_condition)

    @staticmethod
    def value_is(something: str, value: str):
        return Sentences.CONDITION_VALUE_IS.format(something=something, value=value)

    @staticmethod
    def content_is(something: str, content: str):
        return Sentences.CONDITION_CONTENT_IS.format(something=something, content=content)

    @staticmethod
    def in_list(something: str, li: List[str]):
        lists = "\n".join(map(to_str, [(i, item) for i, item in enumerate(li)]))
        return Sentences.CONDITION_IN_LIST.format(something=something, lists="\n" + lists)

    @staticmethod
    def exists_or_not(number: str, unit: str, something: str, description="", not_exists=False):
        word = "不" if not_exists else ""
        return Sentences.CONDITION_EXISTS.format(not_exists=word, number=number, unit=unit,
                                                 something=something,
                                                 description=description)

    @staticmethod
    def exists_in_somewhere_or_not(location: LocationSentences, number: str, unit: str, something: str,
                                   description="",
                                   not_exists=False):
        word = "不" if not_exists else ""
        return Sentences.CONDITION_EXISTS_IN_SOMEWHERE.format(location=location.msg, not_exists=word, number=number,
                                                              unit=unit,
                                                              something=something,
                                                              description=description)

    @staticmethod
    def when_exists_or_not(when: str, number: str, unit: str, something: str, description: str, not_exists=False):
        word = "不" if not_exists else ""
        return Sentences.CONDITION_EXISTS_WITH_WHEN.format(when=when, not_exists=word, number=number, unit=unit,
                                                           something=something,
                                                           description=description)

    @staticmethod
    def when_exists_in_somewhere_or_not(when: str, somewhere: str, number: str, unit: str, something: str,
                                        description: str,
                                        not_exists=False):
        word = "不" if not_exists else ""
        return Sentences.CONDITION_EXISTS_IN_SOMEWHERE.format(when=when, somewhere=somewhere, not_exists=word,
                                                              number=number,
                                                              unit=unit,
                                                              something=something,
                                                              description=description)


def to_str(data: Tuple[int, str]) -> str:
    index, d = data
    return f"{index}. {d};"


if __name__ == '__main__':
    print(DescriptionSentences.__dict__)

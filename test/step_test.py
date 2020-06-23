import unittest

from define.sentences import StepSentences, LocationSentences, ActionSentences, ExceptSentences
from excel.case import StepDescription, ExceptResult


class MyTestCase(unittest.TestCase):

    def test_case(self):
        desc = StepDescription(1)
        desc.add_step(
            StepSentences(1).make(ActionSentences.click_something_with_location("用户名", LocationSentences.left()))) \
            .add_step(StepSentences(2).make(ActionSentences.click_something_with_location("密码",
                                                                                          LocationSentences.in_particular_somewhere(
                                                                                              "浏览器", "左上角")))
                      ) \
            .add_step(StepSentences(3).make(
            ActionSentences.input_something_with_location("密码", LocationSentences.in_somewhere("弹出的模态框"), "abc")))
        print(desc.serialize())

    def test_result(self):
        ex = ExceptResult(1)
        ex.add_step(StepSentences(1).make(
            ExceptSentences.except_location_display_something("红色按钮", LocationSentences.in_somewhere("模块框")))) \
            .add_step(StepSentences(2).make(ExceptSentences.except_result_is("输入框", "123")))
        print(ex.serialize())


if __name__ == '__main__':
    unittest.main()

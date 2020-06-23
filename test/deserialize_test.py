import unittest

from excel.case import FrontCondition
from lexer.parser import ExprScanner


class MyTestCase(unittest.TestCase):

    def test_something(self):
        scanner = ExprScanner()
        condition = FrontCondition()

        stream = scanner.next("value_is<用户名, 15>")
        name, value = condition.args_parser(stream[0].span())
        self.assertEqual(name, "用户名")
        self.assertEqual(value, "15")

        stream = scanner.next("exists<数据,unit::item,number(1)>")
        print(*condition.args_parser(stream[0].span()))


if __name__ == '__main__':
    unittest.main()

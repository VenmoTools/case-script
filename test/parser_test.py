import re
import unittest

import ddt

from lexer.parser import LineScanner, Token

matcher = re.compile(r"status::.+?", )


@ddt.ddt
class MyTestCase(unittest.TestCase):

    @ddt.data("status_is<status::enable>", "status_is<status::disable>",
              "status_is<status::exists>", "status_is<status::n_exists>",
              "status_is<status::delete>", "status_is<status::n_delete>",
              "status_is<status::active>", "status_is<status::n_active>",
              "status_is<status::cust(启用)>")
    def test_status(self, line):
        scanner = LineScanner()
        word = scanner.next(line)[0]
        self.assertEqual(Token.STATUS, word.token())
        self.assertNotEqual("", word.keyword())
        self.assertNotEqual("", word.span())
        self.assertEqual(matcher.fullmatch(word.span()).group(), word.span())

    @ddt.data("when<无网环境>",
              "when<http://www.aaa.bbb/?aa=5&as=5>不可访问")
    def test_when(self, line):
        scanner = LineScanner()
        word = scanner.next(line)[0]
        self.assertEqual(Token.STATUS, word.token())
        self.assertNotEqual("", word.keyword())
        self.assertNotEqual("", word.span())

    @ddt.data("situation_is<无网环境>",
              "situation_is<http://www.aaa.bbb/?aa=5&as=5>不可访问")
    def test_situation(self, line):
        scanner = LineScanner()
        word = scanner.next(line)[0]
        self.assertEqual(Token.STATUS, word.token())
        self.assertNotEqual("", word.keyword())
        self.assertNotEqual("", word.span())

    @ddt.data(
        ("value_is<用户名, 15>", "用户名, 15"),
        ("value_is<密码, *****>", "密码, *****"),
        ("value_is<密码, http:://aaa.bbb.cc/?ad=123&ab#>", "密码, http:://aaa.bbb.cc/?ad=123&ab#"),
        ("content_is<用户名, 15>", "用户名, 15"),
        ("content_is<密码, *****>", "密码, *****"),
        ("content_is<密码, http:://aaa.bbb.cc/?ad=123&ab#>", "密码, http:://aaa.bbb.cc/?ad=123&ab#"),
        ("exists<数据,unit::item,number(1)>", "数据,unit::item,number(1)"),
    )
    @ddt.unpack
    def test_multi_arg(self, line, value):
        scanner = LineScanner()
        word = scanner.next(line)[0]
        self.assertEqual(Token.CONDITION, word.token())
        self.assertNotEqual("", word.keyword())
        self.assertEqual(value, word.span())

    @ddt.data(
        ("exists<数据,unit.item,number(1)>in<数据库>", "数据,unit.item,number(1)", "数据库"),
        ("request<数据库>status_is<status::enable>", "数据库", "status::enable"),
        ("n_request<数据库>left<aabb>", "数据库", "aabb"),
        ("except<红色字体>change_to<蓝色字体>", "红色字体", "蓝色字体"),
        ("except_result<文本框>is<admin>", "文本框", "admin"),
        ("except_note<请输入用户名>left<用户名输入框>", "请输入用户名", "用户名输入框"),
        ("open<xxx.exe>situation_is<python被删除>", "xxx.exe", "python被删除"),
    )
    @ddt.unpack
    def test_multi_token(self, line, value1, value2):
        scanner = LineScanner()
        words = scanner.next(line)
        word = words[0]
        self.assertIn(word.token(), [Token.CONDITION, Token.EXCEPT_RESULT, Token.ACTION])
        self.assertNotEqual("", word.keyword())
        self.assertEqual(value1, word.span())
        word = words[1]
        self.assertIn(word.token(), [Token.STATUS, Token.LOCATION, Token.EXCEPT_RESULT], f"invalid token {word}")
        self.assertNotEqual("", word.keyword())
        self.assertEqual(value2, word.span())

    @ddt.data(
        ("find<输入>do<input<admin>>", "输入", "input<admin>"),
        ("find<输入>do<input<admin>left<a>>", "输入", "input<admin>")
    )
    @ddt.unpack
    @unittest.skip
    def test_recursive_token(self, line, value1, value2):
        scanner = LineScanner()
        words = scanner.next(line)
        word = words[0]
        self.assertEqual(Token.ACTION, word.token())
        self.assertNotEqual("", word.keyword())
        self.assertEqual(value1, word.span())
        word = words[1]
        self.assertEqual(Token.ACTION, word.token(), f"invalid token {word}")
        self.assertNotEqual("", word.keyword())
        self.assertEqual(value2, word.span())


if __name__ == '__main__':
    unittest.main()

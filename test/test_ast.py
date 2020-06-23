import unittest

from lexer.ast import ConditionASTNode, AST
from lexer.parser import ExprScanner


class MyTestCase(unittest.TestCase):

    def test_condition(self):
        scanner = ExprScanner()
        stream = scanner.next("n_exists<数据,unit.item,number(1)>in<数据库>at<xxx>")

        node1 = ConditionASTNode(stream[0])
        node2 = ConditionASTNode(stream[1])
        node3 = ConditionASTNode(stream[2])
        node1.add_node(node2)
        node2.add_node(node3)

        self.assertEqual(node1.token.keyword(), "n_exists")
        self.assertEqual(node1.next_node().token.keyword(), "in")
        self.assertEqual(node1.next_node().next_node().token.keyword(), "at")

    def test_ast(self):
        scanner = ExprScanner()
        stream = scanner.next("n_exists<数据,unit.item,number(1)>in<数据库>at<xxx>")
        ast = AST()
        ast.from_list(stream)
        self.assertEqual(next(ast).token.keyword(), "n_exists")
        self.assertEqual(next(ast).token.keyword(), "in")
        self.assertEqual(next(ast).token.keyword(), "at")


if __name__ == '__main__':
    unittest.main()

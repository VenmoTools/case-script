from typing import List

from lexer.parser import TokenStream, Token, CONDITION_KW_LIST


class ASTNode:

    def __init__(self, token: TokenStream):
        self.token = token
        self.next = None

    def add_node(self, node):
        self.syntax_check(node)
        self.next = node

    def next_node(self):
        return self.next

    @staticmethod
    def instance_check(node):
        if not isinstance(node, ASTNode):
            raise TypeError(f"except: ASTNode found {node.__class__}")

    def node_kw_cannot_be(self, node, kw):
        if node.token.keyword() == kw:
            raise SyntaxError(f"{self.token.keyword()}`s next key word can not be {kw} ")

    @staticmethod
    def get_node_token(node) -> Token:
        return node.token.token()

    def next_token_must_be(self, token: Token):
        next_token = self.get_node_token(self.next)
        if next_token != token:
            raise ValueError(f"except {token} found {next_token}")

    def next_token_must_in(self, node, tokens: List[Token], msg=None):
        next_token = self.get_node_token(node)
        if not len([x for x in filter(lambda x: x != next_token, tokens)]):
            raise ValueError(msg if msg else f"node token {next_token} not in {tokens}")

    @staticmethod
    def list_without(li, without_element):
        return [x for x in li if x != without_element]

    def kw_cannot_in(self, node, li: List[str]):
        next_kw = node.token.keyword()
        self_kw = self.token.keyword()
        if next_kw in li and self_kw == li:
            raise SyntaxError(f"next key word can not be {next_kw} if current key word is {self_kw}")

    def if_kw_is_then_next_kw_cannot_be(self, self_kw, node, next_kw):
        if self.token.keyword() == self_kw and node.token.keyword() == next_kw:
            raise SyntaxError(f"next key word can not be {next_kw} if current key word is {self_kw}")

    def syntax_check(self, node):
        pass


class ConditionASTNode(ASTNode):

    def syntax_check(self, node: ASTNode):
        """
        value_is<用户名, 15>
        content_is<输入框,20>
        exists<数据,unit.item,number(1)>in<数据库>
        n_exists<数据,unit.item,number(1)>in<数据库>
        request<数据库>status<status::enable>
        n_request<数据库>status<status::enable>
        exists<数据,unit.item,number(1)>in<数据库>at<xxx>
        n_exists<数据,unit.item,number(1)>in<数据库>at<xxx>
        :param node:
        :return:
        """
        self.next_token_must_in(node, [Token.LOCATION, Token.CONDITION, Token.STATUS],
                                f"condition node only accept {Token.CONDITION} or f{Token.LOCATION} or {Token.STATUS}\
                                token "
                                )
        self_kw = self.token.keyword()
        # key word at is end key word
        if self_kw == "at":
            raise TypeError(
                "key word `at<>` is last element you can not use like this \
                `request<something>at<somewhere>request<another>` "
            )
        # check next key word cannot be ["value_is", "content_is", "exists", "in_list",
        #     "n_exists", "request", "n_request"]
        self.kw_cannot_in(node, self.list_without(CONDITION_KW_LIST, "at"))


class StatusASTNode(ASTNode):
    def syntax_check(self, node: ASTNode):
        pass


class LocationASTNode(ASTNode):
    def syntax_check(self, node: ASTNode):
        pass


class ActionASTNode(ASTNode):
    def syntax_check(self, node: ASTNode):
        pass


class ExceptASTNode(ASTNode):
    def syntax_check(self, node: ASTNode):
        pass


class AST:

    def __init__(self):
        self.root = None
        self.temp = None
        self.tk = Token.INVALID
        self.token_mapping = {
            Token.LOCATION: LocationASTNode,
            Token.STATUS: StatusASTNode,
            Token.CONDITION: ConditionASTNode,
            Token.ACTION: ActionASTNode,
            Token.EXCEPT_RESULT: ExceptASTNode,
        }

    def from_list(self, li: List[TokenStream]):
        for token in li:
            self.add_node(self.get_type(token))

    def get_type(self, token: TokenStream) -> ASTNode:
        return self.token_mapping[token.token()](token)

    def add_node(self, node):
        if self.root is None:
            self.root = node
            self.tk = node.token.token()
            self.temp = self.root
        else:
            self._add_node(self.root, node)

    def __next__(self):
        if self.temp is None:
            self.temp = self.root
            raise StopIteration()
        node = self.temp
        self.temp = self.temp.next
        return node

    def __iter__(self):
        return self

    @staticmethod
    def _add_node(root: ASTNode, node: ASTNode):
        cur_node = root
        while cur_node.next:
            cur_node = cur_node.next
        cur_node.next = node

import xlwt
from xlwt import XFStyle

from define.sentences import StepSentences, ActionSentences, LocationSentences, ExceptSentences
from excel.case import Cell, TestCase, CaseName, CaseDescription, FrontCondition, StepDescription, ExceptResult, Note, \
    ActualResult, Column, EmptyCell


class Project:

    def __init__(self, sheet: xlwt.Worksheet):
        self.sheet = sheet
        self.style = XFStyle()
        self.start_line = 0

    def write_start_row(self):
        from excel.case import Column
        for x in sorted([v for k, v in Column.__dict__.items() if "__" not in k], key=lambda tup: tup[0]):
            col, text = x
            self.sheet.write(self.start_line, col, text)

    def write_cell(self, cell: Cell):
        row, col = cell.position()
        self.sheet.write(row, col, cell.content())
        return self

    def write_test_case(self, t_case: TestCase):
        for c in t_case.to_list():
            self.write_cell(c)
        return self


if __name__ == '__main__':
    book = xlwt.Workbook()
    proj = Project(book.add_sheet("Case"))
    proj.write_start_row()
    for i in range(1, 5):
        case = TestCase(i)
        case.set(Column.NAME, CaseName("登录测试"))
        case.set(Column.DESCRIPTION, CaseDescription("test"))
        case.set(Column.CONDITION, FrontCondition())
        desc = StepDescription()
        desc.add_step(
            StepSentences(1).make(ActionSentences.click_something_with_location("用户名", LocationSentences.left()))) \
            .add_step(StepSentences(2).make(ActionSentences.click_something_with_location("密码",
                                                                                          LocationSentences.in_particular_somewhere(
                                                                                              "浏览器", "左上角")))
                      ) \
            .add_step(StepSentences(3).make(
            ActionSentences.input_something_with_location("密码", LocationSentences.in_somewhere("弹出的模态框"), "abc")))
        case.set(Column.STEP, desc)
        ex = ExceptResult()
        ex.add_step(StepSentences(1).make(
            ExceptSentences.except_location_display_something("红色按钮", LocationSentences.in_somewhere("模块框")))) \
            .add_step(StepSentences(2).make(ExceptSentences.except_result_is("输入框", "123")))
        case.set(Column.EXCEPT, ex)
        case.set(Column.NOTE, Note())
        case.set(Column.ACTUAL, ActualResult())
        case.set(Column.MODULE, EmptyCell())
        case.set(Column.EXE_TIME, EmptyCell())
        case.set(Column.STATUS, EmptyCell())
        case.set(Column.TESTER, EmptyCell())
        proj.write_test_case(case)
    book.save("case.xls")

# _*_ coding: utf-8 _*_


"""
接口自动化运行入口
"""
from Api_Assistant.common.configparam_util import ConfigEngine
from Api_Assistant.common.log_util import Logger
from Api_Assistant.common.excel_util import ExcelUtil
from Api_Assistant.testcase.run_case import RunCase
import re
import ddt
import unittest
from Api_Assistant.common.request_util import RequestUtil
from Api_Assistant.common.assert_util import AssertUtil
import random

file_name = ConfigEngine.get_config("caseFileSetting", "caseFile")
sheet_name = ConfigEngine.get_config("caseFileSetting", "sheetName")
logger = Logger("RunMain").get_logger_with_level()
runCase = RunCase(file_name, sheet_name)
excelUtil = ExcelUtil(file_name, sheet_name)
excelUtil.load_excel()
data_list = excelUtil.get_case_list()
RequestUtil = RequestUtil()


@ddt.ddt
class RunMain(unittest.TestCase):
    """
    测试用例执行
    """

    @classmethod
    def setUpClass(cls):

        cls.file_name = file_name
        cls.sheet_name = sheet_name
        cls.logger = logger
        cls.runCase = runCase
        cls.excelUtil = excelUtil

    @ddt.data(*data_list)
    def test_run_case(self, data):

        self.excelUtil.load_excel()


        cookies = self.excelUtil.get_data_by_col_no(self.runCase.COOKIES)

        pattern = '^\$\{(.[^\.]+)\}$'

        cookie_list = []

        match_result = None

        for cookie_depend in cookies:
            if cookie_depend is not None:

                match_result = re.match(pattern, cookie_depend)

            if match_result:
                cookie_list.append(match_result.group(1))

        self.runCase.cookie_dict = dict.fromkeys(cookie_list, '')

        result = self.runCase.run_case_by_data(data)

        self.assertTrue(result)



# _*_ coding: utf-8 _*_


"""
请求基础处理类（数据依赖处理、执行请求、结果解析）
"""
from Api_Assistant.common.request_util import RequestUtil
from Api_Assistant.common.excel_util import ExcelUtil
from Api_Assistant.common.data_util import DataUtil
from Api_Assistant.common.assert_util import AssertUtil
from Api_Assistant.common.log_util import Logger
from requests.cookies import RequestsCookieJar
import re


class RunCase(object):
    """
    执行用例类（数据依赖处理、执行请求、结果解析）
    """

    """定义常量，指定表格每一列"""
    CASE_ID = 1  # 用例编号
    MODULE_NAME = 2  # 项目名称
    CASE_NAME = 3  # 用例名称
    RUN_FLAG = 4  # 用例是否运行
    URL = 5  # 接口url
    REQUEST_METHOD = 6  # 请求类型post/get
    HEADERS = 7  # 请求头
    COOKIES = 8  # 数据依赖
    REQUEST_PARAM = 9  # 请求体
    EXP_RESULT = 10  # 期望响应结果
    STATUS_CODE = 11  # 响应code
    RESPONSE_TEXT = 12  # 实际响应结果
    ASSET_TYPE = 13  # 断言类型
    ASSET_PATTERN = 14  # 断言规则
    EXEC_RESULT = 15  # 是否成功pass/fail

    def __init__(self, file_name, sheet_name=None, sheet_index=0):

        self.requestUtil = RequestUtil()
        self.excelUtil = ExcelUtil(file_name, sheet_name, sheet_index)
        self.dataUtil = DataUtil()
        self.assetUtil = AssertUtil()
        self.logger = Logger(self.__class__.__name__).get_logger_with_level()
        self.cookie_dict = {}

    def run_case_by_data(self, data):
        row_no = 2

        for key in data:
            row_no = key
            break

        row_data = data.get(row_no)

        self.logger.info("执行用例：%s-%s-%s" % (
            row_data[RunCase.CASE_ID - 1], row_data[RunCase.MODULE_NAME - 1], row_data[RunCase.CASE_NAME - 1]))

        case_id = row_data[self.CASE_ID - 1]

        run_flag = row_data[self.RUN_FLAG - 1]
        if run_flag == '否':

            return
        elif run_flag == '是':
            url = row_data[self.URL - 1]
            request_method = row_data[self.REQUEST_METHOD - 1]
            headers = row_data[self.HEADERS - 1]

            if headers is None:
                headers = {}
            else:
                headers = self.dataUtil.str_to_json(headers)

            cookies = row_data[self.COOKIES - 1]

            if cookies:

                depend_cookie = self.cookie_depend(cookies)

                if depend_cookie is not None:
                    if type(depend_cookie) == RequestsCookieJar:
                        cookies = depend_cookie

                    elif depend_cookie == '':
                        cookies = {}

                    else:
                        cookies = self.dataUtil.str_to_json(depend_cookie)

            request_param = row_data[self.REQUEST_PARAM - 1]

            if request_param is not None:
                request_param = self.data_depend(request_param)

            exp_result = row_data[self.EXP_RESULT - 1]

            asset_type = row_data[self.ASSET_TYPE - 1]

            asset_pattern = row_data[self.ASSET_PATTERN - 1]

            self.logger.info("请求URL：%s" % url)
            self.logger.info("请求参数：%s" % request_param)
            self.logger.info("请求头：%s" % headers)
            self.logger.info("请求cookie：%s" % cookies)

            response = None

            if request_method == 'get':

                response = self.requestUtil.do_get(url, request_param, headers, cookies)

            elif request_method == 'post':

                json_param = self.dataUtil.str_to_json(request_param)

                response = self.requestUtil.do_post(url, json_param, '', headers, cookies)

            response_text = response.text.strip()

            if case_id in self.cookie_dict:
                self.cookie_dict[case_id] = response.cookies

            self.logger.info("请求结果：%s\n" % response_text)

            self.excelUtil.set_data_by_row_col_no(row_no, self.STATUS_CODE, response.status_code)
            self.excelUtil.set_data_by_row_col_no(row_no, self.RESPONSE_TEXT, response_text)

            result = self.asset_handle(exp_result, response_text, asset_type, asset_pattern)
            if result:
                self.excelUtil.set_data_by_row_col_no(row_no, self.EXEC_RESULT, 'pass')
            else:
                self.excelUtil.set_data_by_row_col_no(row_no, self.EXEC_RESULT, 'fail')
            return result

    def data_depend(self, request_param):

        request_param_final = None

        match_results = re.findall(r'\$\{.+?\..+?\}', request_param)

        if match_results is None or match_results == []:
            return request_param


        else:
            for var_pattern in match_results:
                start_index = var_pattern.index("{")
                end_index = var_pattern.rindex("}")

                pattern = var_pattern[start_index + 1:end_index]
                spilit_index = pattern.index(".")

                case_id = pattern[:spilit_index]
                proper_pattern = pattern[spilit_index + 1:]
                row_no = self.excelUtil.get_row_no_by_cell_value(case_id, self.CASE_ID)
                response = self.excelUtil.get_data_by_row_col_no(row_no, self.RESPONSE_TEXT)

                result = self.dataUtil.json_data_analysis(proper_pattern, response)

                request_param_final = request_param.replace(var_pattern, str(result), 1)

            return request_param_final

    def cookie_depend(self, request_param):

        cookie_final = None

        match_results = re.match(r'^\$\{(.[^\.]+)\}$', request_param)
        if match_results:

            depend_cookie = self.cookie_dict[match_results.group(1)]  # match_results.group(1)就是 (\d+) 匹配到的数字
            return depend_cookie
        else:

            cookie_final = self.data_depend(request_param)
            return cookie_final

    def asset_handle(self, exp_result, response_text, asset_type, asset_pattern):

        asset_flag = None
        if asset_type == '相等':
            if asset_pattern is None or asset_pattern == '':

                asset_flag = self.assetUtil.equals(response_text, exp_result)
            else:

                exp_value = self.dataUtil.json_data_analysis(asset_pattern, exp_result)

                response_value = self.dataUtil.json_data_analysis(asset_pattern, response_text)

                asset_flag = self.assetUtil.equals(exp_value, response_value)

        elif asset_type == '包含':

            asset_flag = self.assetUtil.contains(response_text, exp_result)

        elif asset_type == '正则':

            asset_flag = self.assetUtil.re_matches(response_text, exp_result)

        return asset_flag

# _*_ coding: utf-8 _*_

"""
数据处理类（数据格式转换、json解析）
"""
from jsonpath_rw import jsonpath, parse
import json


class DataUtil(object):

    def json_data_analysis(self, pattern, str_data):

        dict_data = json.loads(str_data)

        json_exe = parse(pattern)

        madle = json_exe.find(dict_data)

        result = [math.value for math in madle]

        if result is None or result == []:
            return None
        else:
            return result[0]

    def json_to_str(self, strs):

        result = json.dumps(strs, ensure_ascii=False, sort_keyss=True, indent=2)
        return result

    def str_to_json(self, jsons):

        result = json.loads(jsons)
        return result

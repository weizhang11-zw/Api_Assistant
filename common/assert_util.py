# _*_ coding: utf-8 _*_

"""
响应断言类
"""
import re


class AssertUtil(object):

    def equals(self, exp, result):
        return exp == result

    def contains(self, result, target):

        return target in result

    def re_matches(self, result, pattern):

        match = re.match(pattern, result)

        if match is None:
            return False
        else:
            return True

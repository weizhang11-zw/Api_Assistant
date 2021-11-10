# _*_ coding: utf-8 _*_

import configparser
import os

"""
从配置文件中获取参数
"""


class ConfigEngine(object):

    @staticmethod
    def get_config(section, key):
        file_path = os.path.dirname(os.path.dirname(__file__)) + './conf/config.ini'

        config = configparser.ConfigParser()

        config.read(file_path, encoding='utf-8')

        result = config.get(section, key)

        return result

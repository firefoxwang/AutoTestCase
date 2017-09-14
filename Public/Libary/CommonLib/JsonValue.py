# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from objectpath import *
from robot.api import logger
import json
import sys
import copy


class JsonValue:
    def __init__(self):
        self.__value_json = None
        self._expect_json = None
        self.__actual_json = None
        self.base_path = "$."

    def _equal_field(self, path, value, value1):
        __path = copy.deepcopy(path)

        if isinstance(value, list):
            self._get_tree_value(path)
            for i in range(len(value)):
                path = __path + "[" + str(i) + "]"
                self._equal_field(path, value[i], self._tree_value)
        elif isinstance(value, dict):
            self._get_tree_value(path)
            for k, v in value.iteritems():
                path = ".".join((__path, k))
                self._equal_field(path, v, self._tree_value)
        else:
            if isinstance(value1, list):
                if value not in value1:
                    msg = 'JSON查询结果比较,值{0}不在list {1} 内部'.format(value, value1)
                    self._assert_error(msg)
            else:
                self._get_tree_value(path)
                if self._tree_value != value:
                    msg = 'JSON查询结果比较：\n路径{0}返回值为：{1}，期望：{2}'.format(path, self._tree_value, value)
                    self._assert_error(msg)

    def _get_tree_value(self, path):

        self._tree_value = self._tree.execute(path)

    def __convert_json(self, value_str):

        if isinstance(value_str, (str, unicode)):

            self.__value_json = json.loads(value_str, encoding='utf-8')

        elif isinstance(value_str, dict):

            self.__value_json = value_str

        else:

            logger.error("期望结果的数据类型错误")

            sys.exit()

    def get_result_value(self, result, path):
        """
        result : 输入值 \n

        path : 期望获取的值 path \n

        example : \n
        result: {"a":"b","b":["a","b",] , "c" :{"a":"b"} ,"d":{ "c":[1,2,3] } } \n
        except result : d - c 第二个值 , 注：从  0 开始 \n

        | ${x}= | get_result_value | result | d.c[2] | \n"

        """
        # 组合 path
        path = self.base_path + path

        # 转换 类型
        self.__convert_json(result)

        result_value = Tree(self.__value_json).execute(path)

        return result_value

    def assert_equal_json(self, actual_json, expect_json):
        """
        actual_json : 实际结果  为字符串 \n
        expect_json : 期望结果 \n
        example  \n
                    实际结果: {"a":"b","b":["a","b",] , "c" :{"a":"b"} ,"d":{ "c":[1,2,3] } } \n
                    若期望比较: b 中的第二个元素 值是否为  b \n
        expect_json 写法：{"b[1]":"b"}  \n
                    若期望比较: c 中的 a 元素是否 为  b  \n
        expect_json 写法：{"c.a":"b"} \n
                    若期望比较: d 中的 c 列表中的 第二个元素 为 3 \n
        expect_json 写法：{"d.c[2]":3} \n
        example : \n

        | assert_equal_json | actual_json | expect_json | \n"

        """
        if '{' not in expect_json and actual_json == expect_json:
            return

        self.__convert_json(actual_json)

        self.__actual_json = self.__value_json

        self.__convert_json(expect_json)

        self._expect_json = self.__value_json

        self._tree = Tree(self.__actual_json)

        for key, value in self._expect_json.iteritems():
            base_path = self.base_path + key

            self._equal_field(base_path, value, self._expect_json)

    def _assert_error(self, msg):

        raise AssertionError(msg)
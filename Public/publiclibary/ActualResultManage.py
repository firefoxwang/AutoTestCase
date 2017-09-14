# -*- coding:utf-8 -*-
'''
Created on 2016-6-6
 
@author: Rudolf Han
'''
import types
import json
import sys

def GetMapValue(string_info ,*keys):
    print  string_info
    string_info_new=dict(string_info)
    
    print type(string_info_new)
     
    for key in keys:
        if type(string_info_new[key]) is types.StringType and "{" in string_info_new[key] :
            string_info_new=eval(string_info_new[key].split(',"codeAmount')[0]+"}")
            print type(string_info_new)
        else:
            string_info_new=string_info_new[key]
        
    return string_info_new

def ManageToList(actual_result):
    '''
            把返回的JSON穿处理成处理成  list 结果与实际的结果进行比较，
           返回CODE,content 的数量
    '''
    actual_result_list=[]
    actual_result_list.append(actual_result["code"])
    if actual_result.has_key('content'):
        if type(actual_result['content']) is types.StringType and  eval(actual_result['content']).has_key('respCode'):
            actual_result_list.append(eval(actual_result["content"])["respCode"])
        
        elif actual_result['content']==None:
            actual_result_list.append(0)
        else:
            actual_result_list.append(len(eval(actual_result["content"])))
    else:
        actual_result_list.append(0)
    return actual_result_list

def ManageToMap(actual_result):
    '''
            把返回的JSON穿处理成处理成  Map结果
           返回CODE,content 的值
    '''
    actual_result_map={}
    actual_result_map['code']=actual_result["code"]
    if actual_result.has_key('content'):
        actual_result_map["content"]=actual_result["content"]
    else:
        actual_result_map["content"]=None
    return actual_result_map
def split_equal_value (value,split_value="="):
    
    value_info=value.split(split_value)[1]
        
    return value_info


# -*- coding:utf-8 -*-

def _init():#初始化
    global _global_env
    _global_env = None
    global _global_flag
    _global_flag = None

def set_env(value):
    global _global_env
    _global_env = value


def set_jenkins(value):
    global _global_flag
    _global_flag = value



def get_env(defValue='defValue'):
    try:
        return _global_env
    except:
        return defValue

def jekins_remote(defValue='defValue'):
    try:
        return _global_flag
    except:
        return defValue
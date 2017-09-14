# -*- coding:utf-8 -*-
'''
Created on 2016-12-15

@author: dellpc
'''
import redis

from PublicData import *

'''
目前删除 与 查询 ,修改 在后期进行重构
'''

def redis_connect(pro_type,db):
    client =  redis.Redis(host=redis_config[pro_type]["host"], port=redis_config[pro_type]["port"],
                          password=redis_config[pro_type]["password"], db=int(db))
    
    return client

def del_redis_data(pro_type, db, redis_key):
    '''
    pro_type 环境类型 (UAT ,SIT)
    redis_key : key 中的key值 可以 模糊匹配  uss_*
    '''
    client = redis_connect(pro_type.upper(), db)
    
    keys_list = client.keys(redis_key) 

    print keys_list

    key_count = len(keys_list)
    
    for key in keys_list:
        client.delete(key)
    
    print u"--删除  redis_key : {0} 的个数 为  {1} ".format(redis_key, key_count)
    
def serch_redis_value(pro_type,redis_key,db):
    
    client = redis_connect(pro_type.upper(),db)
    key_value = client.get(redis_key)
    return key_value
    
# del_redis_data('sit', '6',"CAPITAL_CONF*")

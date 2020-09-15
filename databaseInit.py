# -*- coding = utf-8 -*-
# @Time : 2020/8/27 8:39 下午
# @Author : 陈达维
# @File : databaseInit.py
# @Software : PyCharm
import redis

import model

#初始化数据库，建表
if __name__ == "__main__":
    model.database_init()



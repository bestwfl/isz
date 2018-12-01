# -*- coding:utf8 -*-

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'sys_user'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String)

# 初始化数据库连接:
engine = create_engine('mysql+pymysql://wangfanglong:#4odRYD$qvPWMGj#2cnphiEiOGte@192.168.0.227:13306/isz_erp')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
user = session.query(User).filter(User.user_name == 'test_王方龙_00')
session.close()
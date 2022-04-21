from django.test import TestCase
import pymssql
import re
# Create your tests here.

# mno='800007'
# mname='鹤顶红'
# mtype='毒药'
# mprice=25.6
# m_p_t='2001-03-12'
# m_v_t='2021-6-26'
# print(str(mno).encode('raw_unicode_escape').decode())
#
# db = pymssql.connect(host='127.0.0.1',user='sa',password='buzhidao',database='YAO')
# cursor = db.cursor()
# sql="insert into medicine(mno,mname,mtype,mprice,m_product_time,m_valid_time) values('%s','%s','%s',%f,'%s','%s')"
# cursor.execute(sql % (mno,mname,mtype,mprice,m_p_t,m_v_t))
# db.commit()
# cursor.close()
# db.close()
# all_users = cursor.fetchall()
# print(all_users)

db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
cursor = db.cursor()
cursor.execute('select * from medicine')
user_list = cursor.fetchall()
print(user_list)
mno='800001'
i=0
has_regiter = 0
while i < len(user_list):
    if mno  in user_list[i]:
        ##表示该数据不存在
        has_regiter = 1
    print(user_list[i])
    i += 1
print(has_regiter)

# def check(order):
#     if len(order) < 8 :
#         return False
#     strengthRegex = re.compile('[a-zA-Z]+')   # 至少有一个字母
#     if strengthRegex.findall(order) == []:
#         return False
#     strengthRegex = re.compile('\d+')         # 至少有一个数字
#     if strengthRegex.findall(order) == []:
#         return False
#     return True
#
# passWord='ab123456'
# print(not check(passWord))
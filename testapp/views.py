from django.shortcuts import render
from django.urls import path
from . import views
from django.contrib import admin
from django.shortcuts import HttpResponse
import pymssql
import re

# Create your views here.
# def login(ask):
#     return render(ask,'login.html')

#初始主页面
def index(request):
    return render(request,'index.html')

def check(order):
    if len(order) < 8 :
        return False
    strengthRegex = re.compile('[a-zA-Z]+')   # 至少有一个字母
    if strengthRegex.findall(order) == []:
        return False
    strengthRegex = re.compile('\d+')         # 至少有一个数字
    if strengthRegex.findall(order) == []:
        return False
    return True
#登录页面
def login_register(request):
    #指定要访问的页面，render的功能：讲请求的页面结果提交给客户端
    return render(request,'substitute.html')

#定义一个函数，用来保存注册的数据
def save(request):
    has_regiter = 0#用来记录当前账号是否已存在，0：不存在 1：已存在
    a = request.GET#获取get()请求
    #print(a)
    #通过get()请求获取前端提交的数据
    userName = a.get('username')
    passWord = a.get('password')
    if not check(passWord):
        return HttpResponse('密码需要包括字母和数字，且不小于八位数！')
    #print(userName,passWord)
    #连接数据库
    db = pymssql.connect(host='127.0.0.1',user='sa',password='buzhidao',database='YAO')
    #创建游标
    cursor = db.cursor()
    #SQL语句
    sql1 = 'select * from admin1'
    #执行SQL语句
    cursor.execute(sql1)
    #查询到所有的数据存储到all_users中
    all_users = cursor.fetchall()
    i = 0
    while i < len(all_users):
        if userName in all_users[i]:
        ##表示该账号已经存在
            has_regiter = 1
        i += 1
    if has_regiter == 0:
        # 将用户名与密码插入到数据库中
        sql2 = 'insert into admin1(name,pwd) values(%s,%s)'
        cursor.execute(sql2,(userName,passWord))
        db.commit()
        cursor.close()
        db.close()
        return HttpResponse('注册成功')
    else:
        cursor.close()
        db.close()
        return HttpResponse('该账号已存在')

def query(request):
    a = request.GET
    userName = a.get('username')
    passWord = a.get('password')
    if not check(passWord):
        return HttpResponse('密码需要包括字母和数字，且不小于八位数！')
    user_tup = (userName,passWord)
    db = pymssql.connect(host='127.0.0.1',user='sa',password='buzhidao',database='YAO')
    cursor = db.cursor()
    sql = 'select * from admin1'
    cursor.execute(sql)
    all_users = cursor.fetchall()
    cursor.close()
    db.close()
    has_user = 0
    i = 0
    while i < len(all_users):
        if user_tup == all_users[i]:
            has_user = 1
        i += 1
    if has_user == 1:
        return render(request, 'Amain.html')
        #return HttpResponse('登录成功')
    else:
        return HttpResponse('用户名或密码有误')

def  admin1_show(request):
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    cursor = db.cursor()
    cursor.execute("select name,pwd from admin1")
    admin_list=cursor.fetchall()
    cursor.close()
    db.close()
    return render(request,"admin1_show.html",{'admin_list':admin_list})


def  medicine_show(request):
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    cursor = db.cursor()
    cursor.execute("select medicine.mno,mname,mtype,mprice,convert(varchar(50),m_product_time,7),convert(varchar(50),m_valid_time,7) from medicine ")
    medicine_list=cursor.fetchall()
    cursor.close()
    db.close()
    return render(request,"medicine_info.html",{'medicine_list':medicine_list})

def  manu_show(request):
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    cursor = db.cursor()
    cursor.execute("select pno,pname,padress,ptel from manufacturer")
    manu_list=cursor.fetchall()
    cursor.close()
    db.close()
    return render(request,"manu_show.html",{'manu_list':manu_list})

def  warehouse_show(request):
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    cursor = db.cursor()
    cursor.execute("select wno,wname,wstore from warehouse")
    ware_list=cursor.fetchall()
    cursor.close()
    db.close()
    return render(request,"warehose_show.html",{'ware_list':ware_list})

def  churu_show(request):
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    cursor = db.cursor()
    cursor.execute("select medicine.mno,mname,warehouse.wno,wname,num,convert(varchar(50),c_time,7) from medicine join store on medicine.mno=store.mno join warehouse on warehouse.wno=store.wno")
    churu_list=cursor.fetchall()
    cursor.close()
    db.close()
    return render(request,"show_churu.html",{'churu_list':churu_list})

#插入模块的form表单
def open_form_insert_medicine(request):
    return render(request,'insert_medicine.html')
def open_form_insert_warehouse(request):
    return render(request,'insert_warehouse.html')
def open_form_insert_manu(request):
    return render(request,'insert_manu.html')
def open_form_insert_churu(request):
    return render(request,'insert_churu.html')

def insert_medicine(request):
    has_regiter = 0  # 用来记录当前数据是否已存在，0：不存在 1：已存在
    a = request.GET  # 获取get()请求
    # print(a)
    # 通过get()请求获取前端提交的数据
    mno = a.get('mno')
    mname=a.get('mname')
    mtype=a.get('mtype')
    mprice=float(a.get('mprice'))
    m_p_t=a.get('m_product_time')
    m_v_t=a.get('m_valid_time')
    # print(userName,passWord)
    # 连接数据库
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    # 创建游标
    cursor = db.cursor()
    # SQL语句
    sql1 = 'select * from medicine'
    # 执行SQL语句
    cursor.execute(sql1)
    # 查询到所有的数据存储到all_users中
    all_medicine = cursor.fetchall()
    i = 0
    while i < len(all_medicine):
        if mno in all_medicine[i]:
            ##表示该数据已经存在
            has_regiter = 1
        i += 1
    if has_regiter == 0:
        # 将用户名与密码插入到数据库中
        sql2 = "insert into medicine(mno,mname,mtype,mprice,m_product_time,m_valid_time) values('%s','%s','%s',%f,'%s','%s')"
        cursor.execute(sql2 % (mno,mname,mtype,mprice,m_p_t,m_v_t))
        db.commit()
        cursor.close()
        db.close()
        return HttpResponse('插入成功')
    else:
        cursor.close()
        db.close()
        return HttpResponse('该数据已存在')

def insert_warehouse(request):
    has_regiter = 0  # 用来记录当前数据是否已存在，0：不存在 1：已存在
    a = request.GET  # 获取get()请求
    # print(a)
    # 通过get()请求获取前端提交的数据
    wno = a.get('wno')
    wname=a.get('wname')
    wstore=int(a.get('wstore'))
    # print(userName,passWord)
    # 连接数据库
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    # 创建游标
    cursor = db.cursor()
    # SQL语句
    sql1 = 'select * from warehouse'
    # 执行SQL语句
    cursor.execute(sql1)
    # 查询到所有的数据存储到all_users中
    all_medicine = cursor.fetchall()
    i = 0
    while i < len(all_medicine):
        if wno in all_medicine[i]:
            ##表示该数据已经存在
            has_regiter = 1
        i += 1
    if has_regiter == 0:
        # 将用户名与密码插入到数据库中
        sql2 = "insert into warehouse values('%s','%s',%d)"
        cursor.execute(sql2 % (wno,wname,wstore))
        db.commit()
        cursor.close()
        db.close()
        return HttpResponse('插入成功')
    else:
        cursor.close()
        db.close()
        return HttpResponse('该数据已存在')

def insert_manu(request):
    has_regiter = 0  # 用来记录当前数据是否已存在，0：不存在 1：已存在
    a = request.GET  # 获取get()请求
    # print(a)
    # 通过get()请求获取前端提交的数据
    pno = a.get('pno')
    pname=a.get('pname')
    padress=a.get('padress')
    ptel=a.get('ptel')
    # print(userName,passWord)
    # 连接数据库
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    # 创建游标
    cursor = db.cursor()
    # SQL语句
    sql1 = 'select * from manufacturer'
    # 执行SQL语句
    cursor.execute(sql1)
    # 查询到所有的数据存储到all_users中
    all_medicine = cursor.fetchall()
    i = 0
    while i < len(all_medicine):
        if pno in all_medicine[i]:
            ##表示该数据已经存在
            has_regiter = 1
        i += 1
    if has_regiter == 0:
        # 将用户名与密码插入到数据库中
        sql2 = "insert into manufacturer values('%s','%s','%s','%s')"
        cursor.execute(sql2 % (pno,pname,padress,ptel))
        db.commit()
        cursor.close()
        db.close()
        return HttpResponse('插入成功')
    else:
        cursor.close()
        db.close()
        return HttpResponse('该数据已存在')

def insert_churu(request):
    has_regiter = 0  # 用来记录当前数据是否已存在，0：不存在 1：已存在
    a = request.GET  # 获取get()请求
    # print(a)
    # 通过get()请求获取前端提交的数据
    mno = a.get('mno')
    wno = a.get('wno')
    num=int(a.get('num'))
    c_time=a.get('c_time')
    # print(userName,passWord)
    # 连接数据库
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    # 创建游标
    cursor = db.cursor()
    # SQL语句
    sql1 = 'select * from store'
    # 执行SQL语句
    cursor.execute(sql1)
    # 查询到所有的数据存储到all_users中
    all_medicine = cursor.fetchall()
    i = 0
    while i < len(all_medicine):
        if [mno,wno,c_time] in all_medicine[i]:
            ##表示该数据已经存在
            has_regiter = 1
        i += 1
    if has_regiter == 0:
        # 将用户名与密码插入到数据库中
        sql2 = "insert into store values('%s','%s',%d,'%s')"
        sql3="update warehouse set wstore=wstore-%d where wno='%s'"
        cursor.execute(sql2 % (mno,wno,num,c_time))
        cursor.execute(sql3 % (num,wno))


        db.commit()
        cursor.close()
        db.close()
        return HttpResponse('插入成功')
    else:
        cursor.close()
        db.close()
        return HttpResponse('该数据已存在')

    
#删除模块的form表单
def open_form_delete_medicine(request):
    return render(request,'delete_medicine.html')
def open_form_delete_warehouse(request):
    return render(request,'delete_warehouse.html')
def open_form_delete_manu(request):
    return render(request,'delete_manu.html')
def open_form_delete_churu(request):
    return render(request,'delete_churu.html')
def delete_medicine(request):
    has_regiter = 0  # 用来记录当前数据是否已存在，0：不存在 1：已存在
    a = request.GET  # 获取get()请求
    # print(a)
    # 通过get()请求获取前端提交的数据
    mno = a.get('mno')
    # print(userName,passWord)
    # 连接数据库
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    # 创建游标
    cursor = db.cursor()
    # SQL语句
    sql1 = 'select * from medicine'
    # 执行SQL语句
    cursor.execute(sql1)
    # 查询到所有的数据存储到all_users中
    all_medicine = cursor.fetchall()
    i = 0
    # while i < len(all_medicine):
    #     if mno not in all_medicine[i]:
    #         ##表示该数据不存在
    #         has_regiter = 1
    #     i += 1
    if has_regiter == 0:
        # 数据存在即删除
        sql2 = "delete medicine where mno='%s'"
        cursor.execute(sql2 % (mno))
        db.commit()
        cursor.close()
        db.close()
        return HttpResponse('删除成功')
    else:
        cursor.close()
        db.close()
        return HttpResponse('该数据不存在')

def delete_warehouse(request):
    has_regiter = 0  # 用来记录当前数据是否已存在，0：不存在 1：已存在
    a = request.GET  # 获取get()请求
    # print(a)
    # 通过get()请求获取前端提交的数据
    wno = a.get('wno')
    # print(userName,passWord)
    # 连接数据库
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    # 创建游标
    cursor = db.cursor()
    # SQL语句
    sql1 = 'select * from warehouse'
    # 执行SQL语句
    cursor.execute(sql1)
    # 查询到所有的数据存储到all_users中
    all_medicine = cursor.fetchall()
    i = 0
    # while i < len(all_medicine):
    #     if wno not in all_medicine[i]:
    #         ##表示该数据不存在
    #         has_regiter = 1
    #     i += 1
    if has_regiter == 0:
        # 数据存在即删除
        sql2 = "delete warehouse where wno='%s'"
        cursor.execute(sql2 % (wno))
        db.commit()
        cursor.close()
        db.close()
        return HttpResponse('删除成功')
    else:
        cursor.close()
        db.close()
        return HttpResponse('该数据不存在')

def delete_manu(request):
    has_regiter = 0  # 用来记录当前数据是否已存在，0：不存在 1：已存在
    a = request.GET  # 获取get()请求
    # print(a)
    # 通过get()请求获取前端提交的数据
    pno = a.get('pno')
    # print(userName,passWord)
    # 连接数据库
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    # 创建游标
    cursor = db.cursor()
    # SQL语句
    sql1 = 'select * from manufacturer'
    # 执行SQL语句
    cursor.execute(sql1)
    # 查询到所有的数据存储到all_users中
    all_medicine = cursor.fetchall()
    i = 0
    # while i < len(all_medicine):
    #     if pno not in all_medicine[i]:
    #         ##表示该数据不存在
    #         has_regiter = 1
    #     i += 1
    if has_regiter == 0:
        # 数据存在即删除
        sql2 = "delete manufacturer where pno='%s'"
        cursor.execute(sql2 % (pno))
        db.commit()
        cursor.close()
        db.close()
        return HttpResponse('删除成功')
    else:
        cursor.close()
        db.close()
        return HttpResponse('该数据不存在')

def delete_churu(request):
    has_regiter = 0  # 用来记录当前数据是否已存在，0：不存在 1：已存在
    a = request.GET  # 获取get()请求
    # print(a)
    # 通过get()请求获取前端提交的数据
    mno = a.get('mno')
    wno = a.get('wno')
    num = int(a.get('num'))
    # print(userName,passWord)
    # 连接数据库
    db = pymssql.connect(host='127.0.0.1', user='sa', password='buzhidao', database='YAO')
    # 创建游标
    cursor = db.cursor()
    # SQL语句
    sql1 = 'select * from store'
    # 执行SQL语句
    cursor.execute(sql1)
    # 查询到所有的数据存储到all_users中
    all_medicine = cursor.fetchall()
    i = 0
    # while i < len(all_medicine):
    #     if (wno,mno) not in all_medicine[i]:
    #         ##表示该数据不存在
    #         has_regiter = 1
    #     i += 1
    if has_regiter == 0:
        # 数据存在即删除
        sql2 = "delete store where mno='%s' and wno='%s'"
        sql3 = "update warehouse set wstore=wstore+%d where wno='%s'"
        cursor.execute(sql2 % (mno,wno))
        cursor.execute(sql3 % (num, wno))
        db.commit()
        cursor.close()
        db.close()
        return HttpResponse('删除成功')
    else:
        cursor.close()
        db.close()
        return HttpResponse('该数据不存在')

#修改模块的form表单
def open_form_alter_medicine(request):
    return render(request,'alter_medicine.html')
def open_form_alter_warehouse(request):
    return render(request,'alter_warehouse.html')
def open_form_alter_manu(request):
    return render(request,'alter_manu.html')
def open_form_alter_churu(request):
    return render(request,'alter_churu.html')
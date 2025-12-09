import pymysql

class DB_util(object):
    def __init__(self):
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.pwd = '123456'
        self.database = 'ai250802'


    def db_user_login(self, acc, pwd):
        """
        登录
        :param acc: 账号
        :param pwd: 密码
        :return: 1 0
        """
        try:
            # 获取数据库连接
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.pwd, database=self.database, charset='utf8')
            # 获取游标
            cursor = conn.cursor()
            # 执行语句
            sql = f"SELECT uid, uname, createtime, imgpath, ustate FROM users WHERE uname = '{acc}' AND upwd = MD5('{pwd}') AND ustate = 1"
            cursor.execute(sql)
            print(cursor.fetchall())

            res = list(cursor.fetchall())
            print(res)
            if len(res) > 0:
                return res
            else:
                return 0

        except pymysql.Error as e:
            print(e)
            conn.rollback()
            return 0
        finally:
            cursor.close()
            conn.close()



    def db_user_reg(self, acc, pwd):
        """
        注册
        :param acc: 账号
        :param pwd: 密码
        :return: 1 0
        """
        try:
            # 获取数据库连接
            conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.pwd, database=self.database, charset='utf8')
            # 获取游标
            cursor = conn.cursor()
            # 执行语句
            sql = f"INSERT INTO users (uname, upwd, createtime, imgpath, ustate) VALUES ('{acc}', MD5('{pwd}'), now(), 'img/img.jpg', 1)"
            i = cursor.execute(sql) # i是受影响行数
            print(i)
            conn.commit()
            if i > 0:
                return 1
            else:
                return 0

        except pymysql.Error as e:
            print(e)
            conn.rollback() # 回滚 在上述方法中如果插入了多张表，前面的表都插入成功了，最后一个失败，那么前面所有插入的数据要还原
            return 0
        finally:
            cursor.close()
            conn.close()


    def db_user_pwdchange(self, acc, pwd):
        """
        修改密码
        :param acc: 账号
        :param pwd: 密码
        :return: 1 0
        """
        # try:
        #     # 获取数据库连接
        #     conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.pwd, database=self.database, charset='utf8')
        #     # 获取游标
        #     cursor = conn.cursor()
        #     # 执行语句
        #     sql = f"INSERT INTO users (uname, upwd, createtime, imgpath, ustate) VALUES ('{acc}', MD5('{pwd}'), now(), 'img/img.jpg', 1)"
        #     i = cursor.execute(sql) # i是受影响行数
        #     print(i)
        #     conn.commit()
        #     if i > 0:
        #         return 1
        #     else:
        #         return 0
        #
        # except pymysql.Error as e:
        #     print(e)
        #     conn.rollback() # 回滚 在上述方法中如果插入了多张表，前面的表都插入成功了，最后一个失败，那么前面所有插入的数据要还原
        #     return 0
        # finally:
        #     cursor.close()
        #     conn.close()


if __name__ == '__main__':
    db = DB_util()
    print(db)
    # db.db_user_login('lisi', '123123')
    res = db.db_user_reg('luu', '123123')
    print(res)

import pymysql

class DButil:
    """数据库工具类"""

    def __init__(self, host='localhost', port=3306, user='root',
                 password='123456', database='ai250802', charset='utf8'):
        """
        初始化数据库连接参数
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset

    def _get_connection(self):
        """获取数据库连接"""
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset
        )

    def _execute_query(self, sql, params=None, fetch_one=False):
        """
        执行查询语句的通用方法
        :param sql: SQL语句
        :param params: 参数元组或字典
        :param fetch_one: 是否只获取一条记录
        :return: 查询结果
        """
        conn = None
        cursor = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()

            return result

        except pymysql.Error as e:
            print(f"数据库查询错误: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _execute_update(self, sql, params=None):
        """
        执行更新语句的通用方法（INSERT, UPDATE, DELETE）
        :param sql: SQL语句
        :param params: 参数元组或字典
        :return: 受影响的行数
        """
        conn = None
        cursor = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            if params:
                affected_rows = cursor.execute(sql, params)
            else:
                affected_rows = cursor.execute(sql)

            conn.commit()
            return affected_rows

        except pymysql.Error as e:
            print(f"数据库更新错误: {e}")
            if conn:
                conn.rollback()
            return 0

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def user_login(self, username, password):
        """
        用户登录验证
        :param username: 用户名（假设唯一）
        :param password: 密码
        :return: 登录成功返回True，失败返回False
        """
        sql = """
            SELECT 1 
            FROM users 
            WHERE uname = %s AND upwd = MD5(%s) AND ustate = 1
            LIMIT 1
        """

        result = self._execute_query(sql, (username, password), fetch_one=True)

        # 如果查询到结果（任意数据），说明登录成功
        return result is not None

    def user_register(self, username, password, img_path='img/img.jpg'):
        """
        用户注册
        :param username: 用户名（保证唯一）
        :param password: 密码
        :param img_path: 头像路径
        :return: 注册成功返回True，失败返回False
        """
        # 由于数据库中username已保证唯一，这里直接尝试插入
        # 如果违反唯一约束会抛出异常
        sql = """
            INSERT INTO users (uname, upwd, createtime, imgpath, ustate) 
            VALUES (%s, MD5(%s), NOW(), %s, 1)
        """

        try:
            affected_rows = self._execute_update(sql, (username, password, img_path))
            return affected_rows > 0

        except pymysql.IntegrityError as e:
            # 用户名重复错误
            if 'Duplicate entry' in str(e):
                print(f"用户名 '{username}' 已存在")
            else:
                print(f"数据库完整性错误: {e}")
            return False

    def user_change_password(self, username, new_password):
        """
        修改用户密码
        :param username: 用户名
        :param new_password: 新密码
        :return: 修改成功返回True，失败返回False
        """
        sql = """
            UPDATE users 
            SET upwd = MD5(%s) 
            WHERE uname = %s AND ustate = 1
        """

        affected_rows = self._execute_update(sql, (new_password, username))
        return affected_rows > 0

    def get_user_info(self, username):
        """
        获取用户信息（可选，如果需要获取用户详细信息）
        :param username: 用户名
        :return: 用户信息，不存在返回None
        """
        sql = """
            SELECT uid, uname, createtime, imgpath, ustate 
            FROM users 
            WHERE uname = %s AND ustate = 1
        """

        result = self._execute_query(sql, (username,), fetch_one=True)

        if result:
            # 返回字典格式的用户信息
            return {
                'uid': result[0],
                'uname': result[1],
                'createtime': result[2],
                'imgpath': result[3],
                'ustate': result[4]
            }
        return None

    def get_user_by_id(self, user_id):
        """
        根据用户ID获取用户信息
        :param user_id: 用户ID
        :return: 用户信息字典，不存在返回None
        """
        sql = """
            SELECT uid, uname, createtime, imgpath, ustate 
            FROM users 
            WHERE uid = %s AND ustate = 1
        """

        result = self._execute_query(sql, (user_id,), fetch_one=True)

        if result:
            return {
                'uid': result[0],
                'uname': result[1],
                'createtime': result[2],
                'imgpath': result[3],
                'ustate': result[4]
            }
        return None


# 使用示例
if __name__ == '__main__':
    # 创建数据库工具实例
    db = DButil()

    print("=" * 50)
    print("数据库操作测试")
    print("=" * 50)

    # 1. 用户登录测试
    print("\n1. 登录测试:")

    # 正确登录测试
    if db.user_login('lyz', '549293'):
        print("✓ 'lyz' 登录成功")
    else:
        print("✗ 'lyz' 登录失败")

    # 错误密码测试
    if not db.user_login('lyz', 'wrong_password'):
        print("✓ 错误密码被正确拒绝")
    else:
        print("✗ 错误密码应该被拒绝")

    # 2. 用户注册测试
    print("\n2. 注册测试:")

    # 生成唯一的测试用户名
    import time

    test_username = f"test_user_{int(time.time())}"

    # 注册新用户
    if db.user_register(test_username, 'test123'):
        print(f"✓ 用户 '{test_username}' 注册成功")

        # 测试刚注册的用户能否登录
        if db.user_login(test_username, 'test123'):
            print(f"✓ 新注册用户登录成功")
        else:
            print("✗ 新注册用户登录失败")
    else:
        print(f"✗ 用户 '{test_username}' 注册失败")

    # 3. 修改密码测试
    print("\n3. 修改密码测试:")

    if db.user_change_password('lyz', 'new_password'):
        print("✓ 密码修改成功")

        # 用新密码登录
        if db.user_login('lyz', 'new_password'):
            print("✓ 新密码登录成功")
        else:
            print("✗ 新密码登录失败")

        # 改回原密码以便后续测试
        db.user_change_password('lyz', '549293')
        print("✓ 密码已改回原密码")
    else:
        print("✗ 密码修改失败")

    # 4. 获取用户信息测试
    print("\n4. 获取用户信息测试:")

    user_info = db.get_user_info('lyz')
    if user_info:
        print(f"✓ 获取用户信息成功:")
        for key, value in user_info.items():
            print(f"  {key}: {value}")
    else:
        print("✗ 获取用户信息失败")

    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)
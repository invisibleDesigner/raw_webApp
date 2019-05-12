import pymysql

connection = pymysql.connect(
            host='localhost',
            user='root',
            password='123qwe',
            # db='test',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
)
sql = 'CREATE DATABASE `user` DEFAULT CHARACTER SET utf8mb4'
sql_use = 'USE user'
sql_create = '''
    CREATE TABLE `user` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `username` VARCHAR(45) NOT NULL,
        `password` CHAR(64) NOT NULL,
        PRIMARY KEY (`id`)
    )'''
sql_insert = "insert into user value ('1', 'yyy', '123')"
sql_select = "select * from user"
with connection.cursor() as c:
    # c.execute(sql)
    c.execute(sql_use)
    c.execute(sql_select)
    print(c.fetchall())
connection.commit()
connection.close()

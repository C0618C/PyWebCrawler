
import pymysql.cursors


# 连接MySQL数据库
connection = pymysql.connect(host='192.168.0.4', port=3306, user='vmwed', password='vmwed.com', db='web1', 
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

# 通过cursor创建游标
cursor = connection.cursor()

# 创建sql 语句，并执行
sql = "INSERT INTO `Article` (`Title`, `Content`) VALUES ('Test DB', 'Success')"
cursor.execute(sql)

# 提交SQL
connection.commit()
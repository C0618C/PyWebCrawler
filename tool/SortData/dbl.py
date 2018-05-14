
import pymysql.cursors




def RecordOneItem(item,ittype):
    # 连接MySQL数据库
    connection = pymysql.connect(host='192.168.0.4', port=3306, user='vmwed', password='vmwed.com', db='web1', 
                    charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    # 通过cursor创建游标
    cursor = connection.cursor()
    try:
        # 创建sql 语句，并执行
        cursor.execute("INSERT INTO `Article`(`Title`, `Content`,`CreateDate`,`SrcURL`,`Type`) VALUES(%s, %s,%s,%s,%s)"
        ,(item["title"][0],item["down"][0],item["date"][0],item["src_url"][0],ittype))
        cursor.execute("SELECT LAST_INSERT_ID() rowid")
        row_1 = cursor.fetchone()
        
        i = 0
        for img in item["images"]:
            print(img["path"])
            cursor.execute("INSERT INTO `Picture`(`ArticleId`, `Name`,`Path`,`OrderNo`,`SrcURL`,`Type`) VALUES(%s, %s,%s,%s,%s,%s)"
            ,(row_1["rowid"],item["title"][0],img["path"],i,img["url"],(0 if(img["url"] == item["preview"][0]) else 1) ))
            i+=1
    except Exception as e:
        print("ERROR:RecordOneItem::",e)
        connection.rollback()

    # 提交SQL
    connection.commit()

    # 关闭连接
    cursor.close()
    connection.close()
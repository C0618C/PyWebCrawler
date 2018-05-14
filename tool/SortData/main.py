# import os

# import sortsetting as st
# print("test")
# print(st.sort_setting)

import json
import dbl



# 打开文件
fo = open("tool/sortdata/test/item_result.json", "r")
# print ("文件名为: ", fo.readline())

for line in fo.readlines():
    info1 = json.loads(line)
    dbl.RecordOneItem(info1,1)

# 关闭文件
fo.close()



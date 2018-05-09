import os

import sqlite3 as sql
import boto3



DATABASE = 'labelme.db'
con = sql.connect(DATABASE)
cur = con.cursor()

cur.execute("SELECT dns,id from users")
dns = cur.fetchall()


key_path = "./Key_Pairs/MutipleUse.pem"
for user_dns in dns:
    os.system('scp -i {} -r ubuntu@{}:~/test_folder ~/{}'.format(key_path, user_dns[0], user_dns[1]))
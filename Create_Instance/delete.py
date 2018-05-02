import boto3
import sys

import sqlite3 as sql

ec2 = boto3.resource('ec2', region_name = "us-west-1")


DATABASE = 'labelme.db'
con = sql.connect(DATABASE)
cur = con.cursor()


cur.execute("SELECT dns from users where id= '{}'" .format(sys.argv[1]))
dns = cur.fetchone()

# python delete.py <instance_id> <key_pair_name> 
# check what instance are running and delete specific instance
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    if(instance.public_dns_name == dns[0]):
        response = instance.terminate()
        #print response

cur.execute("DELETE from users where id= '{}'" .format(sys.argv[1]))
con.commit()


con.close()

for instance in instances:  
    print(instance.id, instance.instance_type)

'''
#delete key pair 
ec2_del = boto3.client('ec2', region_name = "us-west-1")
response = ec2_del.delete_key_pair(
    KeyName=sys.argv[2],
    #DryRun=True|False
)
'''
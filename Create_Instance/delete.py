import boto3
import sys

ec2 = boto3.resource('ec2', region_name = "us-west-1")

# python delete.py <instance_id> <key_pair_name> 
# check what instance are running and delete specific instance
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    if(instance.id == sys.argv[1]):
        response = instance.terminate()
        #print response

for instance in instances:  
    print(instance.id, instance.instance_type)

#delete key pair 
ec2_del = boto3.client('ec2', region_name = "us-west-1")
response = ec2_del.delete_key_pair(
    KeyName=sys.argv[2],
    #DryRun=True|False
)
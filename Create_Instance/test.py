
import boto3


'''
ec2 = boto3.resource('ec2', region_name = "us-west-1")


# check what instance are running
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    if(instance.id == 'i-0de3e812b17f3c534'):
        response = instance.terminate()
        #print response

for instance in instances:  
    print(instance.id, instance.instance_type)
'''

ec2 = boto3.client('ec2', region_name = "us-west-1" )
response = ec2.describe_key_pairs()
print(response)

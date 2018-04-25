
import boto3


ec2 = boto3.resource('ec2', region_name = "us-west-1" )

running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

#ec2info = defaultdict()

for instance in running_instances:
    print(instance.public_dns_name)

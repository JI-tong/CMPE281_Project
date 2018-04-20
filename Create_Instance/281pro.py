import boto.ec2
import boto3

#ec2 = boto3.client('ec2')
#response = ec2.describe_instances()
#print(response)
#ec2 = boto3.resource('ec2', region_name = "us-west-1")

def create_KeyPair(name):
	temp = "./Key_Pairs/"
	temp += name
	temp +=".pem"
	outfile = open(temp, 'w')
	key_pair = ec2.create_key_pair(KeyName=name)
	KeyPairOut = str(key_pair.key_material)
	outfile.write(KeyPairOut)
	return name

def create_Instance(name, min, max):
	instances = ec2.create_instances(
		ImageId='ami-c57261a5', 
		MinCount=int(min), 
		MaxCount=int(max),
		KeyName=name,
		InstanceType="t2.micro",
		SecurityGroupIds = ['sg-b0e167c9']
	)
	print("instance with key pair [{}] created\n".format(name))
	return instances

if __name__ == '__main__':
	ec2 = boto3.resource('ec2', region_name = "us-west-1")
	message = input("Do you want to create a new key pair?(1 = yes/0 = no) > ")
	if(message == '1'):
		cus = input("enter the name you want:")
		create_KeyPair(cus)
	message = input("Do you want to create launch a new instance?(1 = yes/0 = no) > ")
	if(message == '1'):
		cus = input("enter the key pair you want to use:")
		create_Instance(cus,1,1)

	#for instance in instances:  
    #	print(instance.id, instance.instance_type)


'''
#terminate instance and delete Key_pair
ec2_Del = boto3.client('ec2', region_name = "us-west-1")

response = ec2_Del.delete_key_pair(
    KeyName='Test3',
    #DryRun=True|False
)
'''
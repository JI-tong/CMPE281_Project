

from flask import Flask, render_template, request
import boto.ec2
import boto3

app = Flask(__name__)

# instance creation function
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



@app.route('/')
def index():
    return render_template('register.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
        result = request.form
        #for key, value in result.items():
        #    print("{},{}".format(key,value))
        check = result.get('Name')
        create_KeyPair(check)
        create_Instance(check,1,1)
        return render_template('result.html',result = result)

if __name__ == '__main__':
    ec2 = boto3.resource('ec2', region_name = "us-west-1")
    app.run(debug = True)
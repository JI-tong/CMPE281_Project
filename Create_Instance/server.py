

from flask import Flask, render_template, request
import boto.ec2
import boto3

app = Flask(__name__)

usrs = {}

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
	instance = instances[0]
	instance.wait_until_running()
	instance.load()
	dns = instance.public_dns_name
	labelMe = "http://" + dns + "/LabelMeAnnotationTool/tool.html"
	print(labelMe)
	return labelMe



@app.route('/')
def index():
	return render_template('register.html')
    #return render_template('login.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
        result = request.form
        #for key, value in result.items():
        #    print("{},{}".format(key,value))
        usrname = result.get('Name')
        #create_KeyPair(usrname)
        LabelMe = create_Instance('MutipleUse',1,1)
        return render_template('result.html',result = result, LabelMe = LabelMe, usrname = usrname)

if __name__ == '__main__':
    ec2 = boto3.resource('ec2', region_name = "us-west-1")
	# if in the ec2 use:
	# app.run(host='0.0.0.0', port=80)
	# then log in using ec2 instance public ip
    app.run(debug = True)


from flask import Flask, render_template, request,redirect
import boto.ec2
import boto3
import sqlite3 as sql

app = Flask(__name__)
DATABASE = 'labelme.db'
img = "templates/labelme.jpg"

def start_db():
	try:
		db= sql.connect(DATABASE)
		db.execute('CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY NOT NULL, password TEXT NOT NULL, link TEXT NOT NULL, dns TEXT NOT NULL)')
		print("****Initializing database****")


		db.commit()
		msg = "Database initialization finished"
	except:
		db.rollback()
		msg = "Already created"

	finally:
		db.close()
	return msg

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
		ImageId='ami-d8a4bbb8', 
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
	return labelMe, dns



@app.route('/', methods = ['GET','POST'])
def index():
	error = None

	if request.method == 'POST':
		try:
			result = request.form
			username = result.get('uname')
			password = result.get('psw')

			con = sql.connect(DATABASE)
			cur = con.cursor()

			cur.execute("SELECT password,link from users where id= '{}'" .format(username))
			data = cur.fetchone()
			#data[0] password, data[1] link for labelMe
			if data is None:
				error = "UserName not exist"
			elif data[0] != password:
				error = "Wrong password"
			else:
				con.close()
				return redirect(data[1])
		except:
			error = 'SqlError'
		finally:
			con.close()

	return render_template('index.html', error = error, user_image = img)
    #return render_template('login.html')

@app.route('/regist', methods = ['POST','GET'])
def regist(): 
	if request.method == 'POST':
		result = request.form
		#for key, value in result.items():
		#    print("{},{}".format(key,value))
		usrname = result.get('Name')
		password = result.get('Password')
		#create_KeyPair(usrname)
		LabelMe, dns = create_Instance('MutipleUse',1,1)

		con = sql.connect(DATABASE)
		con.execute("INSERT INTO users (id, password, link, dns) VALUES(?,?,?,?)",(usrname, password, LabelMe, dns))
		con.commit()
		con.close()
		return redirect(LabelMe)
	return render_template('register.html')

@app.route('/dbinfo', methods = ['GET'])
def info():
	con = sql.connect(DATABASE)
	con.row_factory = sql.Row

	cur = con.cursor()
	cur.execute("SELECT * FROM users")
	rows = cur.fetchall()

	con.close()
	return render_template('info.html', rows = rows)


if __name__ == '__main__':
    ec2 = boto3.resource('ec2', region_name = "us-west-1")
	# if in the ec2 use:
	# app.run(host='0.0.0.0', port=80)
	# then log in using ec2 instance public ip
    start_db()
    #app.run(debug = True)
    app.run(host='0.0.0.0', port=80)
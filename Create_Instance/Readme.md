## Prepration:

pip3 install virtualenv

virtualenv my-venv
. my-venv/bin/activate # activate the my-venv

//install the necessary packages on your venv
pip3 install flask
pip3 install boto
pip3 install boto3
//also dont forget to configure the aws

## Run:
go to the folder where server.py located

. my-venv/bin/activate
python server.py


in the webpage type:
localhost:5000
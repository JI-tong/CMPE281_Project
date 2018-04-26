# Prepration:

```
pip3 install virtualenv
```

### create & activate the my-venv
```
virtualenv my-venv
. my-venv/bin/activate 
```

### install the necessary packages on your venv
```
pip3 install awscli
pip3 install flask
pip3 install boto
pip3 install boto3
```
### also dont forget to configure the aws
```
aws configure
```

# Run:

go to the folder where server.py located

```
. my-venv/bin/activate
python server.py
```

### in the webpage type:
```
localhost:5000
```
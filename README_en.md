# MIS (Management Information System): Campus AI Assistant

[语言: 中文](./README.md)

## 1. Introduction
This project relies on `Python3.9`, with `Django` and `Mysql`.

As using `YOLOV5` network, you need to install some data analysis package.

## 2. Install
Firstly, create a new file in `Terminal`
```text
mkdir newfile
```
Then get in it
```text
cd newfile
```

Secondly, clone the project in this file
```text
git clone git@github.com:isKage/mis.git
```
Then get into the root director of this project
```text
cd mis
```

## 3. Download
Note: this project relies on `Python3.9`
```text
pip install -r requirements.txt
```

## 4. Mysql settings
At `mis` file, create a file `local_settings.py`
```python
# setting language
LANGUAGE_CODE = 'zh-hans'

# mysql settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mis',  # use your database's name
        'USER': 'root',  # the user of your database
        'PASSWORD': '******',  # the password
        'HOST': '127.0.0.1',  # local host
        'PORT': '3306',  # default port
    }
}
```

Make data tables, run the code at `Terminal`
```text
python3 manage.py makemigrations
python3 manage.py migrate
```
## 5. Run
At `Terminal`
```text
python3 manage.py
```

Then open the link at browser as followed, if been run at the local
> http://localhost:8000/
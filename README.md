Content summary
- [1. Setup](#1-setup)
- [2. Using python-dotenv](#2-using-python-dotenv)


## 1. Setup
Create project with virtual environment

```console
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv
```

Activate it
```console
$ . venv/bin/activate
```

or on Windows
```console
venv\Scripts\activate
```

Install Flask
```console
$ pip install -r requirements
```

Set environment variables in terminal
```console
export FLASK_APP=app.py
export FLASK_ENV=development
```

or on Windows
```console
set FLASK_APP=app.py
set FLASK_ENV=development
```

Run the app
```console
$ flask run
```


## 2. Using python-dotenv
python-dotenv to manage environmints in a file

see mor in: https://pypi.org/project/python-dotenv/

Common cli list:
List the env variables
```console
$ dotenv list
```
Set USER value
```console
$ dotenv set USER foo
```
Get stored value
```console
$ dotenv get USER
```


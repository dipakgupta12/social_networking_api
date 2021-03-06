# social_ntw_api
social networking api

***
* python 3.8.6
* Other dependencies under social_ntw_api/requirements.txt


### Python virtual env
```
$ python3.8 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

### Run Django app
```
$ python manage.py migrate
$ python manage.py runserver
```

### Run celery in background.
``` 
$ celery -A social_ntw_api worker -l INFO
NOTE:
* Make sure you are in project root directory. ex: social_ntw_api). 
* Redis server must be installed and running on redis://localhost:6379/0
```

### Run test cases. All tests are available in api/posts/tests.py
```
$ python manage.py test
```

### API documentation
```
Swagger : http://localhost:8000/swagger/
redoc :  http://localhost:8000/redoc/

```

#### CI config file can be found in .circleci/config.yml. For each commit in **mail** branch CI will trigger at [circleci](https://app.circleci.com/pipelines/github/dipakgupta12/social_networking_api?branch=main). Deployed on heroku : [heroku](https://test-app-for-django.herokuapp.com/admin/login/?next=/admin/) .

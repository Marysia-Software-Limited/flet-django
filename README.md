# Django Flutter Framework

Django based desktop/mobile/web application.

## Instalation
- Install all python packages:

        $ pip install -r requirements.txt
- Migrate database:

        $ python manage.py migrate

## Run and usage
- To run app use todo django command:

        $ python manage.py todo
- To run server use --view parameter:

        $ python manage.py todo --view flet_app_hidden
- Server will be avaible as http://$APP_HOST:$APP_PORT, default value is 8085, for example:

        $ open http://ala.hipisi.org.pl:8085
- Compile ./frontend futter app to have separate ready to install application:

        $ cd frontend
        $ flutter run --dart-entrypoint-args http://94.23.247.130:8085
- You can use simple script to run separate flutter application:

        $ python run.py

## Demo

Working demo [is here](http://ala.hipisi.org.pl:8085).

## Screenshots

![Android app](./todo_pixel4.png)

![iOS app](./todo_iphone14.png)

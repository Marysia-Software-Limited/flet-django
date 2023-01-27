# Just married!!!
# Django and Flutter.

## Rapid developing db based app. Zero boilerplate code.

I hate boilerplate code. I hated it all my life. I made so many steps to remove this mental parasites far from me. And now, with Flet and Django I'm so close to get my ideal. For this moment I made as PoC a clone of a standard Flet ToDo application. All what i change is write all directly inside of Django. Flet code is run directly on the backend, so we not need any dedicated communication layer. Next what I done is generic data table control. This is a simple control able to create a data table for any Django model. All with searching and sorting. My roadmap is now:
create generic form for any model
manage relations between models
create datetime, date and time pickers
solve problem with horizontal and vertical scrolling data table
add filtering management for each of columns
pack all as Django package, ready to add to any existing project

## Instalation
- Install python package:

        $ pip install flet-django
- Add 'flet_django' to INSTALLED_APPS in settings.py:
        `INSTALLED_APPS += ['flet_django']`
- Add flet code in file main_app.py

## Run and usage
- To run app use todo django command:

        $ python manage.py run_app
- To run server use --view parameter:

        $ python manage.py run_app --view flet_app_hidden
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

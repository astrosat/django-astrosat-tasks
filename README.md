# django-astrosat-tasks

## quick start

1.  in the project you want to use it type:
    `pipenv install -e git+https://github.com/astrosat/django-astrosat-tasks.git@master#egg=django-astrosat`

2.  add "astrosat_users" to your INSTALLED_APPS settings like this:

```
     INSTALLED_APPS = [
         ...
         'astrosat_tasks',
         ...
    ]
```

3.  add lots of settings; look at "astrosat_tasks/conf/settings.py" to see what to add

4.  include the astrosat URLconf in your project "urls.py" like this:

```
 path("", include("astrosat_tasks.urls")
```

5.  run `python manage.py migrate` to create the astrosat models.

6.  profit!

## developing

django-astrosat-tasks comes w/ an example project to help w/ developing/testing. b/c it requires a task broker (rabbitmq), it runs in Docker.

1. `git clone <repo> django-astrosat-tasks`
2. `cd django-astrosat-tasks/example`
3. `docker-compose up` (this will start the services: "db", "broker", and "server"; you can run them separately if desired)

4. `python manage.py runserver` goto "http://localhost:8000" and enjoy
5. you can monitor the task queue at "http://localhost:1672"

## notes

note that the reference to django-astrosat-users in "Pipfile" was created with: `pipenv install -e .`. This looks for the "setup.py" file in the current directory. If the distribution changes just run `pipenv update django-astrosat-tasks`, otherwise code changes should just be picked up b/c of the "-e" flag.

note also that in order for runserver to pickup live changes to the code, the Pipfile, Dockerfile, etc. are at the ROOT_DIR rather than in the example  app, and _both_ example and astrosat_tasks are mounted as volumes in docker-compose.yml.

FYI - sometimes pipenv waits for pip to get input from stdin (like w/ github repos); to get around this set `PIPENV_NOSPIN=1` as per https://github.com/pypa/pipenv/issues/3770

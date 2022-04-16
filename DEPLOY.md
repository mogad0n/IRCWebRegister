# Deploying

It is highly recommended to run the application behind a reverse proxy.

Here we will use `nginx`, `gunicorn` a WSGI standalone server and decide between `supervisord` and `systemd`.

## Install gunicorn

* Check that you are still in the virtual environment.
* `pip install gunicorn`.
* TODO
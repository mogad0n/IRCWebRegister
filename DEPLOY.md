# Deploying

Deploy using nginx + uwsgi with an init system.

## Resources

* [flask-docs](https://flask.palletsprojects.com/en/2.1.x/deploying/uwsgi/)

## Procedure

### templates

* Update the templates for `/register` and `/verify` paths.

### uwsgi commands and notes

* `$ uwsgi -s /tmp/yourapplication.sock --manage-script-name --mount /yourapplication=myapp:app`
* If you want to deploy your flask application inside of a virtual environment, you need to also add --virtualenv /path/to/virtual/environment. You might also need to add --plugin python or --plugin python3 depending on which python version you use for your project.

### Nginx Config

The Usual - This configuration binds the application to /yourapplication.

```location = /yourapplication { rewrite ^ /yourapplication/; }
location /yourapplication { try_files $uri @yourapplication; }
location @yourapplication {
  include uwsgi_params;
  uwsgi_pass unix:/tmp/yourapplication.sock;
}
```

If you want to have it in the URL root its a bit simpler:

```location / { try_files $uri @yourapplication; }
location @yourapplication {
    include uwsgi_params;
    uwsgi_pass unix:/tmp/yourapplication.sock;
}

```

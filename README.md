# Docker Nginx SSL Cert Auth +  Flask + Celery + Redis

A basic [Docker Compose](https://docs.docker.com/compose/) template for orchestrating a [Flask](http://flask.pocoo.org/) application & a [Celery](http://www.celeryproject.org/) queue with [Redis](https://redis.io/) behind an nginx reverse proxy with SSL client certificate authentication.

### Installation

Download the sources:

```bash
https://github.com/vladiuz1/docker-flask-celery-redis-hotcode-nginx-ssl-auth
```

### Developement environment

In the developement environment you do not need to do much, as all your code is exposed via ports 5001 (api) and 5555 (flower), and running
on the localhost.

All you need to do is run
```bash
docker-compose -f docker-compose.yml.dev up -d --build
```

It will build all the necessary services for you and start them up on localhost.

Access your endpoints:
* api (api/app.py): `localhost:5001`
* flower: `localhost:5001`

To change the endpoints, update the code in [api/app.py](api/app.py)

Task changes should happen in [queue/tasks.py](celery-queue/tasks.py)

Services will be restarted automatically as you save the files.

### Production environment

##### config 

To deploy, first set your environment: copy `example.env` into `.env`:
```bash
cp example.env .env
```
Then edit the file to enter your hostname, email. Your api will be accessible from `api.<NGINX_HOSTNAME>` and 
flower will be running on `flower.<NGINX_HOSTNAME>`

##### dns

Now point DNS of the domain (api.<domain>, flower.<domain>) to the ip address.

##### ssl

Create Let's Encrypt SSL certificates for domains `api.<your.domain>` and `flower.<your.domain>`
```bash
sudo ./init-letsencrypt.sh
```
This will create ssl certificates in `./data/certbot/conf/live/`

##### launch

You are ready to launch:
```bash
docker-compose up -d --build
```

The api will be available on these URLs:
* `https://api.your.domain`
* `https://flower.your.domain`

`./data/client_certs` contains a ca.crt - a sample ssl certificate authority file that will be used to
authenticate out of the box. Install the client certificate on your browser `user.pfx` to access
the URLs above. 

#### WARNING

You need to create or re-use your own ca.crt and sign client certificates with it.

### Scale

To add more workers:
```bash
docker-compose up -d --scale worker=5 --no-recreate
```

### Shut down

```bash
docker-compose down
```

---

adapted from 
* [https://github.com/itsrifat/flask-celery-docker-scale](https://github.com/itsrifat/flask-celery-docker-scale)
* [https://github.com/mattkohl/docker-flask-celery-redis](https://github.com/mattkohl/docker-flask-celery-redis)
* [https://github.com/dlesz/docker-flask-celery-redis-hotcode](https://github.com/dlesz/docker-flask-celery-redis-hotcode)
* [https://medium.com/@pentacent/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71](https://medium.com/@pentacent/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71)

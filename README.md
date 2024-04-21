# docker-darkice-monitor

Docker container with python and cron to check in Darkice streaming is down, then send e-mail

# Requirements

* [Docker](https://docs.docker.com/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)

# Install

1. Get an .env file

```
cp .env.example .env
```

2. (Optional) adjust settings. In the provided example we will use some b64encoded passwords, which can be obtained with:

```
from base64 import b64encode
print(b64encode('cleartextpassword'.encode('utf-8')))
```

Probably the main variable to update will be `CRON`.

Remember to add below trailing string to each one of the commands in the `CRON` variable to get the output to the stdout of the container, thus allowing `docker logs -f cron` to display content:

```
> /proc/1/fd/1 2>/proc/1/fd/2
```

# Usage

1. Bring up the container

```
sudo docker compose up --build -d
```

Depending on what contains variable `CRON` you will get the result.

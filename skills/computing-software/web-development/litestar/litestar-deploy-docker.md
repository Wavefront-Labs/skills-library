---
id: computing-software.web-development.litestar.litestar-deploy-docker
name: litestar-deploy-docker
category: computing-software
field: web-development
product: litestar
tags: [litestar, docker, compose, deployment, dockerfile, containers, postgres, litestar-run]
level: practitioner
status: docs-checked
description: "Containerise a Litestar app with the documented Dockerfile running litestar run, build and run commands, and a Docker Compose file with a Postgres service."
sources: [https://docs.litestar.dev/latest/topics/deployment/docker.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploy Litestar with Docker

Goal: package the app in a container and optionally run it with a database via Compose.

## Method

1. Project files: `requirements.txt` containing `litestar[standard]>=2.4.0,<3.0.0` (the standard extra provides `uvicorn`) and an `app.py` exposing `app = Litestar(route_handlers=[...])`.
2. Dockerfile from the page:

```docker
FROM python:3.12-slim-bookworm
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
EXPOSE 80
CMD ["litestar", "run", "--host", "0.0.0.0", "--port", "80"]
```

3. Build and run:

```shell
docker build -t exampleapp .
docker run -d -p 80:80 --name exampleapp exampleapp
docker stop exampleapp
docker start exampleapp
docker rm exampleapp
```

4. You can also launch with an ASGI server directly instead of `litestar run`.
5. Compose: define two services. `exampleapp` builds from `context: ./` with `dockerfile: Dockerfile`, sets `container_name`, `depends_on: [database]`, `ports: ["80:80"]` and environment variables `DB_HOST=database`, `DB_PORT=5432`, `DB_USER`, `DB_PASS`, `DB_NAME`. `database` uses `image: postgres:latest` with `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, port `5432` and a named volume `db_data` (the page notes that Postgres images before 18 used `/var/lib/postgresql/data`).
6. Run it:

```shell
docker compose build
docker compose up        # add -d to run in the background
docker compose down
```

## Gotchas

- `depends_on` makes the database start before the app.
- Replace the sample credentials in the compose file before real use.

## Verify

With the container up on port 80, the page's `app.py` serves `{"hello": "world"}` at `/` and at `/sync`.

## Checked

2026-11-07. Read the full cited page(s) (topics/deployment/docker.html) and the example files they include, and confirmed the claims in this skill against that text. Reworded the depends_on note to the page's own wording.

Method: documentation only; no commands were run.

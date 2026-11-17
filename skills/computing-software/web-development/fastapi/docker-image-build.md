---
id: computing-software.web-development.fastapi.docker-image-build
name: docker-image-build
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, docker, dockerfile, container, deployment, exec-form, workers, kubernetes]
level: practitioner
status: docs-checked
description: "Containerize FastAPI with a Dockerfile from the official Python image: layer caching, exec-form CMD, proxy headers, single versus multi-process containers."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/deployment/docker.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FastAPI in Docker

## Dockerfile steps (from the official Python image)
1. `FROM python:3.14` (the docs' example tag).
2. `WORKDIR /code`.
3. `COPY ./requirements.txt /code/requirements.txt` first, alone, so Docker caches the next step.
4. `RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt` (`--no-cache-dir` is a pip option, unrelated to Docker).
5. `COPY ./app /code/app` near the end, since code changes most often and invalidates later layers.
6. `CMD ["fastapi", "run", "app/main.py", "--port", "80"]`.

With uv, export locked deps: `uv export --format requirements-txt --no-dev --no-emit-project --output-file requirements.txt`. A single `main.py` works too (`COPY ./main.py /code/`, `fastapi run main.py`).

## Rules
- Always use the exec form of `CMD` (a list), not shell form, so shutdown is graceful and lifespan events trigger.
- Behind a TLS termination proxy (Nginx, Traefik), add `--proxy-headers`.
- On Kubernetes or similar, replicate at cluster level: one process per container, no `--workers`. For a single server or Docker Compose, `--workers 4` in the CMD can make sense.
- HTTPS is handled outside the image (Traefik or a cloud provider). Restarts come from the runner (e.g. Docker `--restart`).
- Do not use the deprecated tiangolo/uvicorn-gunicorn-fastapi base image; `--workers` replaced it.
- Run previous steps (like migrations) in a separate/init container when replicated.

## Build and run
`docker build -t myimage .` then `docker run -d --name mycontainer -p 80:80 myimage`; check `/docs`.

## Checked

Read the full FastAPI deployment/docker.md source page. Confirmed the Dockerfile steps and the python:3.14 example tag, layer-caching order, uv export command, single-file variant, exec-form CMD (graceful shutdown, lifespan events), --proxy-headers behind a TLS termination proxy, one process per container on clusters versus --workers 4 for a single server or Docker Compose, external HTTPS, --restart, init container for previous steps, and the deprecated tiangolo/uvicorn-gunicorn-fastapi image.

Method: docs-only read of cited pages, 2026-11-08

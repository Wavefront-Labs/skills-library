---
id: computing-software.web-development.vapor.vapor-deploy-docker
name: vapor-deploy-docker
category: computing-software
field: web-development
product: vapor
tags: [vapor, vapor-docker, docker, docker-compose, swarm, deployment, migrations]
level: practitioner
status: docs-checked
description: "Dockerize a Vapor app from the toolbox template: Dockerfile, docker-compose services, build, run, migrate, Swarm scaling and production notes."
sources:
  - https://docs.vapor.codes/deploy/docker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: build and run a Vapor app and its database in containers, locally or on a server.

## Start from the template
Install the Vapor Toolbox and run `vapor new my-dockerized-app`. Your prompt answers affect the generated Docker files. For an existing app, generate the template in a new folder and copy the resources over.

- Dockerfile: two stages. Stage one builds the app; stage two sets up a secure runtime, copies the result, and sets an entrypoint and command that run the app in production mode on port 8080 (overridable).
- docker-compose.yml: services for the app, `migrate`, `revert`, and the database (varies with the database chosen). The image is named `my-dockerized-app:latest`.

Shared environment near the top of the compose file:

```docker
x-shared_environment: &shared_environment
  LOG_LEVEL: ${LOG_LEVEL:-debug}
  DATABASE_HOST: db
  DATABASE_NAME: vapor_database
  DATABASE_USERNAME: vapor_username
  DATABASE_PASSWORD: vapor_password
```

Services pull it in with `<<: *shared_environment`. Hard-coded credentials are fine locally; for production keep them in a secrets file exported to the deploy environment and use `DATABASE_USERNAME: ${DATABASE_USERNAME}`. `LOG_LEVEL` is taken from the host environment, falling back to debug.

Notes: `depends_on` defines dependencies; `ports` is `<host_port>:<service_port>`; `DATABASE_HOST: db` works because Docker's network DNS routes `db` to the service named `db`; a service `command` runs against the Dockerfile `ENTRYPOINT`; in Swarm Mode `migrate` and `revert` have `deploy` `replicas: 0`.

## Build
From the folder with `docker-compose.yml`:

```shell
docker compose build
docker image ls
```

It rebuilds everything inside Docker's Linux environment; host build artifacts are not reused.

## Run standalone
```shell
docker compose up app            # starts app and db; app at http://localhost:8080
docker compose up --detach app   # background
docker container ls
docker logs <container_id>
docker compose run migrate       # run migrations
```

Before migrating, `/todos` returns `{"error":true,"reason":"Something went wrong."}` with `relation "todos" does not exist` in the logs; after migrating it returns an empty list.

- Verbose logs: `LOG_LEVEL=trace docker-compose up app`.
- App and db logs together: `docker-compose up app db`.
- Stop: `docker container stop <container_id>` or `docker-compose down`.
- Wipe the `db_data` volume: `docker-compose down --volumes`, or `docker volume ls`, `docker volume rm my-dockerized-app_db_data`, `docker volume prune` (careful: removes unused volumes). Volumes in use by running or stopped containers cannot be removed (`docker container ls -a`).

## Swarm Mode (test horizontal scaling)
```shell
docker swarm init
docker stack deploy -c docker-compose.yml test
docker service ls                           # expect 1/1 app and db, 0/0 migrate and revert
docker service scale --detach test_migrate=1
docker service scale test_app=5
docker service logs -f test_app
docker stack rm test
```

Quirk: after the migrate service runs and exits it shows 0/1; to migrate again in the same Swarm, scale it to 0 first, then back to 1.

## Production
The guide gives no host-specific steps. A server running the Docker daemon accepts the same commands: copy the project, SSH in, and run `docker-compose` or `docker stack deploy`. Alternatively set local `DOCKER_HOST` to point at the server and run docker locally; then no project files need copying, but the image must be hosted where the server can pull it.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) deploy/docker, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.

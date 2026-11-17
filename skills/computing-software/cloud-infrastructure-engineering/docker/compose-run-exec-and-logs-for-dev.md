---
id: computing-software.cloud-infrastructure-engineering.docker.compose-run-exec-and-logs-for-dev
name: compose-run-exec-and-logs-for-dev
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, dev-workflow, compose-run, one-off-container, compose-exec, compose-logs, migrations]
level: practitioner
status: docs-checked
description: "Run one-off tasks with docker compose run (--rm, --no-deps, -T, --service-ports) and inspect services with compose exec and compose logs options during development."
sources: ["https://docs.docker.com/reference/cli/docker/compose/run/", "https://docs.docker.com/reference/cli/docker/compose/exec/", "https://docs.docker.com/reference/cli/docker/compose/logs/", "https://docs.docker.com/compose/how-tos/profiles/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# compose run, exec and logs in development

## run: one-off containers
```sh
docker compose run --rm api python manage.py migrate
docker compose run --rm --no-deps api pytest -q              # don't start linked services
docker compose run --rm -e DEBUG=1 -v ./out:/out api ./report
docker compose run --rm --service-ports web                  # publish the service's ports
docker compose run --rm -p 127.0.0.1:2021:21 web             # or publish specific ports
docker compose run --rm -T api ./script.sh < input.txt       # no TTY: CI / piping
docker compose run --rm --entrypoint sh api                  # override the entrypoint
docker compose run --rm --build api ...                      # build the image first
```
- `run` starts the service with its configuration (volumes, links and so on), but the
  command you pass overrides the service's `command`.
- If the service has linked services, `run` first checks that they are running and starts
  them if they are stopped; `--no-deps` prevents that.
- `run` does not create the ports in the service configuration, which avoids collisions
  with already-open ports; use `--service-ports` or `-p` to publish.
- `--rm` removes the container when it exits, even if a restart policy is set.
- Without `--rm` the finished container is kept; `docker compose ps -a` shows containers
  created by `run`.
- Other options: `-u/--user`, `-w/--workdir`, `-l/--label`, `--name`, `--cap-add`,
  `--cap-drop`, `-d/--detach`, `--env-from-file`, `--pull`, `--quiet-pull`.

## exec: into running services
```sh
docker compose exec api sh
docker compose exec -u root api apk add curl
docker compose exec -T db pg_dump -U postgres app > dump.sql   # -T: no TTY for redirected output
docker compose exec --index 2 worker ps aux                    # second replica
docker compose exec -w /app/sub -e X=1 api ./tool
```
`exec` is the equivalent of `docker exec` for a service; it allocates a TTY by default (the
reason for `-T` in scripts) and keeps stdin interactive by default.

## logs
```sh
docker compose logs -f api worker
docker compose logs --tail 50 --since 10m -t
docker compose logs --no-log-prefix api                    # drop the "api-1 |" prefix
docker compose logs --no-color > all.log
docker compose up --attach api --no-attach db              # choose which services stream in the foreground
```
`logs` also takes `--index` (replica) and `--until`.

## Patterns
- Migrations: a `migrate` service with `profiles: [tools]` and
  `depends_on: { db: { condition: service_healthy } }`. A service that has profiles runs
  when you target it explicitly, so `docker compose run --rm migrate` works without
  enabling the profile; its `depends_on` services are started too (they must not be gated
  behind a profile you have not enabled).
- Or make the migration a dependency of the app:
  `depends_on: { migrate: { condition: service_completed_successfully } }`.
- Shells for debugging: `exec` when the service runs; `run --rm --entrypoint sh` when it
  does not stay up.

## Verify
`docker compose ps -a` shows no leftover `run` containers when you used `--rm`.

## Checked
Date 2026-10-23. Documentation release: Compose v5.6.1 CLI reference and Docker docs
(docker/docs main). Method: documentation only; no commands were run.
Confirmed every flag used above in the `run`, `exec`, `logs` and `up` references (`--rm`,
`--no-deps`, `-e`, `-v`, `--service-ports`, `-p`, `-T`, `--entrypoint`, `--build`, `--index`,
`-w`, `-u`, `--tail`, `--since`, `-t`, `--no-log-prefix`, `--no-color`, `--attach`,
`--no-attach`), the `run` description (command override, linked services, no ports, `--rm`
overrides restart policy), the `exec` TTY description, the `depends_on` conditions and the
profiles how-to (explicitly targeted services run without enabling the profile). Removed:
the exit-code remark, the run-container naming pattern, and JSON-processing pipelines.

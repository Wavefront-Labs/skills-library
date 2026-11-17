---
id: computing-software.cloud-infrastructure-engineering.docker.env-files-file-suffix-secrets-and-env-leaks
name: env-files-file-suffix-secrets-and-env-leaks
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, secrets, env-file, env-file-format, env-file-quoting, file-suffix-convention, secret-file, env-leak, inspect-env-leak, secret-injection]
level: practitioner
description: "Pass config with docker run --env-file (and its no-quoting rules), prefer secrets as files via the _FILE convention, and know every place env-var secrets leak."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/#env", "https://docs.docker.com/build/building/secrets/", "https://hub.docker.com/_/postgres"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# env files, _FILE secrets and env-var leaks

## docker run --env-file format
```
# comment lines start with #
DB_HOST=db
DB_USER=app
EMPTY=
# a bare name (no '=') takes its value from the docker CLI's environment:
PASSTHROUGH
```
Per the `docker run` reference: lines are `<variable>=value` or `<variable>`, and a line
starting with `#` is a comment, whereas a `#` anywhere else in a line is **part of the value**
(`A=1 # x` sets `1 # x`). A bare name that is not set in your local environment is unset in
the container. The docs do not describe quote or expansion handling for `--env-file`, so do
not rely on either; check the result with `docker inspect`. Windows CRLF endings are a
classic source of stray characters in values.

## Secrets as files: the _FILE convention
The official postgres image accepts `POSTGRES_PASSWORD_FILE` (and `_FILE` forms of some other
variables) pointing at a file containing the value; check each image's README for which
variables support it:
```sh
docker run -e POSTGRES_PASSWORD_FILE=/run/secrets/pg_pw \
  -v "$PWD/secrets/pg_pw:/run/secrets/pg_pw:ro" postgres
```
Implement it in your own entrypoint:
```sh
file_env() {               # usage: file_env DB_PASSWORD
  var=$1; fvar="${var}_FILE"
  eval val=\${$var:-}; eval fval=\${$fvar:-}
  if [ -n "$val" ] && [ -n "$fval" ]; then echo "both $var and $fvar set" >&2; exit 1; fi
  if [ -n "$fval" ]; then export "$var"="$(cat "$fval")"; unset "$fvar"; fi
}
file_env DB_PASSWORD
exec "$@"
```
Better still, have the app read the file directly so the value never enters the environment.

## Where env-var secrets leak
| Place | How |
|---|---|
| `docker inspect` | `.Config.Env` - anyone with Docker API access |
| child processes | inherited by everything the app spawns |
| crash reports and debug pages, logs | anything that dumps the environment |
| image | Docker's build docs: build arguments and environment variables persist in the final image, so use build secrets instead |

## Verify
```sh
docker inspect -f '{{json .Config.Env}}' app     # expect no secret values
docker exec app ls -l /run/secrets               # secret files present
```

## Checked
Date: 2026-10-26. Documentation: docker/docs main (last commit 2026-10-23) `docker run` reference (env section) and build secrets page; docker-library postgres README. Confirmed: env-file line syntax, `#` handling, bare-name behaviour, `POSTGRES_PASSWORD_FILE`, build-arg/ENV persistence. Removed as unconfirmed: quote and expansion claims, CRLF specifics, Compose env_file comparison, `_FILE` support for mysql, mariadb and redis-stack, /proc environ, Django and Sentry examples, `docker history` and `docker compose config` leak rows, the mode 0400 expectation, the pinned postgres tag.
Method: documentation only; no commands were run.

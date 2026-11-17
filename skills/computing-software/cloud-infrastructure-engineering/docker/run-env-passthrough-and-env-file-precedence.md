---
id: computing-software.cloud-infrastructure-engineering.docker.run-env-passthrough-and-env-file-precedence
name: run-env-passthrough-and-env-file-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, environment-config, env-passthrough, env-file, docker-run, environment-variables, secrets]
level: practitioner
status: docs-checked
description: "Pass environment to docker run: -e NAME passthrough from the host, -e NAME=value, multiple --env-file, precedence over image ENV, and keeping values out of shell history."
sources: ["https://docs.docker.com/reference/cli/docker/container/run/#env", "https://github.com/docker/cli/blob/master/cli/command/container/opts.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# docker run env passthrough and --env-file precedence

## Forms
```bash
docker run -e LOG_LEVEL=debug app            # explicit value
export API_KEY=...; docker run -e API_KEY app   # NAME only: copied from the client's environment
docker run --env-file common.env --env-file prod.env app
```
- `-e NAME` without `=` and with `NAME` not exported in the shell: the variable is **unset** in the container. Useful for optional settings.
- Passthrough keeps the value out of the command line, though environment variables are stored in the container configuration and visible in `docker inspect`.

## Precedence (last wins)
1. Image `ENV` (Dockerfile); `--env`, `--env-file` overwrite variables defined in the image
2. `--env-file` files are read first, in the order given
3. `-e` / `--env` values are applied after the files (per the docker/cli source, `ReadKVEnvStrings(envFile, env)`), so they win

```bash
docker run --rm --env-file base.env -e LOG_LEVEL=warn alpine env | sort
```

## --env-file format
```text
# comment
LOG_LEVEL=info
DB_HOST=db
API_KEY
```
- A line beginning with `#` is a comment; a `#` anywhere else in a line is part of the value, so put comments on their own lines (a trailing comment would become part of the value).
- `NAME` alone takes the value from the client's environment; `NAME=value` sets it.
- Compose `env_file` has its own parsing rules; check the Compose documentation rather than assuming they match.

## Inspect the result
```bash
docker exec <c> env | sort
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' <c>
```

## Safer handling of secrets
- Environment variables are stored in the container's configuration and can be read with `docker inspect`; prefer mounted secret files or Compose/Swarm secrets for sensitive values.
- If env is unavoidable, use passthrough or an env file with restrictive permissions rather than typing `-e KEY=value` in shells or CI logs.

## Gotchas
- Passthrough reads the environment of the `docker` CLI process itself, so a variable must be exported in the shell that runs `docker run`.

## Checked

Checked against the `docker container run` reference ("Set environment variables", `data/cli/engine/docker_container_run.yaml`) and the docker/cli source (`cli/command/container/opts.go`, `opts/env.go`) (docker/docs latest commit 2026-10-23, Engine 29).

- `-e NAME` takes the local value, is unset in the container when not exported, `--env-file` syntax (`NAME=value`, `NAME`, `#` comment lines only at line start), env flags overwrite image variables, env files are read before `-e` values.
- Removed as unconfirmed: quote-handling and `export` claims, the `sudo` and PowerShell remarks, and the claim that later env files override earlier ones beyond the order they are read.
- The original example with a trailing `# comment` on a variable line was wrong, because Docker treats that text as part of the value.

Method: documentation only; no commands were run.

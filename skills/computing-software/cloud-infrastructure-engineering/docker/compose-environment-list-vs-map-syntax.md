---
id: computing-software.cloud-infrastructure-engineering.docker.compose-environment-list-vs-map-syntax
name: compose-environment-list-vs-map-syntax
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-env, environment-map, environment-variables, env-passthrough, yaml-booleans, compose-file]
level: practitioner
status: verified
description: "Write Compose environment blocks correctly: list vs map forms, value-less passthrough, YAML booleans and numbers, quotes kept in list form, empty vs unset, and merge behaviour."
sources: ["https://docs.docker.com/reference/compose-file/services/#environment", "https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/", "https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compose environment: list vs map syntax

## Two equivalent forms
```yaml
environment:                 # list
  - RACK_ENV=production
  - SHOW=true
  - SESSION_SECRET           # passthrough from Compose's environment
```
```yaml
environment:                 # map
  RACK_ENV: production
  SHOW: "true"               # quote! unquoted true is a YAML boolean
  SESSION_SECRET:            # null value = passthrough
```

## Traps
| Written | Container gets | Why |
|---|---|---|
| `- PASSWORD="s3cret"` (list) | `"s3cret"` with the quote characters | List items are taken literally after `=` |
| `PASSWORD: "s3cret"` (map) | `s3cret` | YAML quotes are syntax |
| `DEBUG: true` | `"true"` (Compose converts); `yes` stayed `"yes"` on Compose v2.39, but other YAML 1.1 tools may read it as a boolean; unquoted `0755` became `493` (octal) | Always quote booleans and numbers with leading zeros (`"0755"`) |
| `- FOO` with FOO unset in the shell | Variable not set | Passthrough only copies existing values |
| `FOO: ""` | Set to empty string | Different from unset for many apps |
| `- FOO=${FOO}` with FOO unset | Set to empty string + warning | Interpolation defaults to blank |

## Passthrough vs interpolation
- `- TOKEN` (passthrough): value read when the container is created; never written into the
  resolved config (`docker compose config` shows `TOKEN: null`). Good for secrets from CI.
- `- TOKEN=${TOKEN}`: interpolated into the model; visible in `config` output.

## Merging across files
Maps merge by key across `-f` files: an override can change one variable without repeating
the rest. Lists are normalised to maps for merging, so mixing forms between files works, but
keep one form per repository for readability.

## Precedence reminder
`docker compose run -e` > `environment:` > `env_file:` > image `ENV`.

## Verify
```bash
docker compose config --format json | jq '.services.app.environment'
docker compose exec app env | sort
```

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (`docker compose config`, no daemon): list form keeping quote characters (`PASSWORD="s3cret"` gave the value with quotes, as did single quotes) versus map form stripping them; `SHOW: true`, `INT: 42`, `FLOAT: 1.5` all emitted as strings; `0755` emitted as `"493"`; `FOO` and `FOO:` pass-through giving `null` when unset and the value when set (and `config` showing `null`, not the secret); `FOO: ""` giving an empty string; `- BAR=${BAR}` unset giving an empty string plus the warning; list and map forms merging by key across two `-f` files (`A=1,B=1` list plus `B: '2', C: '3'` map gave A=1, B=2, C=3). Not run: containers (`exec env`), YAML 1.1 parsers other than Compose's, Linux.

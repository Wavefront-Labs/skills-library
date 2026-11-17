---
id: computing-software.cloud-infrastructure-engineering.docker.where-compose-interpolation-applies
name: where-compose-interpolation-applies
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, env-interpolation, interpolation-scope, compose-variables, dotenv, double-dollar, project-directory]
level: practitioner
status: docs-checked
description: "Know where ${VAR} is substituted by Compose: Compose file values, .env and env_file, which .env is read, and where it never applies (Dockerfiles, container shells)."
sources: ["https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/", "https://docs.docker.com/reference/compose-file/interpolation/", "https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/", "https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/", "https://docs.docker.com/reference/compose-file/include/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Where Compose interpolation applies

## Substituted by Compose
- Any **value** in the Compose file. Interpolation applies only to YAML values, not keys;
  where keys are user-defined strings (for example `labels` or `environment`), use the
  equal-sign list form (`- "$VAR=BAR"`) for interpolation to apply to the key.
- Interpolation is applied per file, before merging.
- Supported braced forms: `${VAR}`, `${VAR:-default}` and `${VAR-default}`,
  `${VAR:?error}` and `${VAR?error}`, `${VAR:+replacement}` and `${VAR+replacement}`; nesting
  such as `${VARIABLE:-${FOO}}` works. Other shell-style forms (`${VARIABLE/foo/bar}`) are not
  supported. Unbraced `$VAR` also works for valid names.
- Sources, highest precedence first: the shell environment, then a file given with
  `--env-file`, then (if `--env-file` is not set) the `.env` file in the project directory.
- In `.env` files, unquoted and double-quoted values have interpolation applied.

## Not substituted by Compose
| Location | What happens instead |
|---|---|
| Dockerfile | Only Dockerfile `ARG`/`ENV` rules apply at build time; pass values through `build.args` |
| The container's shell | Compose processes any `$` followed by a valid variable name first, so write `$$VAR` to leave it for the container |
| Keys of the Compose file | Not interpolated (see above) |

```yaml
services:
  app:
    image: "reg.example.com/app:${TAG:?TAG is required}"
    command: ["sh", "-c", "echo container home is $$HOME, tag ${TAG}"]
```
`$$` produces a literal dollar sign and prevents Compose from interpolating a value.

## Which .env file?
When `--env-file` is not set, Compose reads `.env` from the **project directory**:
`--project-directory` if set, otherwise the directory of the first Compose file given with
`-f`, otherwise the shell's current directory. `--env-file` replaces the default; you can use
several `--env-file` options and later files override variables from earlier ones. If that
`.env` sets `COMPOSE_FILE` to a path in a different directory, Compose may load a second
`.env` from that directory with lower precedence.

## Debug
```bash
docker compose config                     # fully interpolated model
docker compose config --no-interpolate    # raw values
docker compose config --environment       # environment used for interpolation
```
If Compose cannot resolve a variable and no default is defined, it displays a warning and
substitutes an empty string.

## Gotchas
- A variable defined in `.env` is available for interpolation; to reach a container's
  environment it must be referenced in `environment:` (for example `- DEBUG=${DEBUG}`) or
  supplied through `env_file:`.
- `.env` substitution is a Compose CLI feature; it is not supported by `docker stack deploy`.
- A literal `$` in a value inside the Compose file must be written `$$`.
- For `include:`, the `project_directory` defaults to the included file's directory and its
  `env_file` defaults to `.env` in that directory, and can be set per include entry.

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main), Compose v5.6.1.
Method: documentation only; no commands were run.
Confirmed in the Compose interpolation reference, variable-interpolation how-to,
environment-variable precedence page and `include` reference: syntax list, keys versus
values, `$$`, per-file interpolation, warning-and-empty-string behaviour, source precedence,
project-directory rule, repeated `--env-file`, `.env` quoting rule, Swarm limitation, include
defaults. Removed: the exact warning text, the claim that passthrough environment entries
are never interpolated, and the "mounted files are copied verbatim" remark.

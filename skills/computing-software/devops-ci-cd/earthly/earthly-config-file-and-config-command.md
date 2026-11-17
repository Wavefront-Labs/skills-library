---
id: computing-software.devops-ci-cd.earthly.earthly-config-file-and-config-command
name: earthly-config-file-and-config-command
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, config, config-yml, earthly-config, dry-run, cache-size-mb, global]
level: practitioner
status: docs-checked
description: "Edit the earthly config file at ~/.earthly/config.yml by hand or with earthly config key value, including --dry-run, YAML values and keys containing periods."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthly-config/earthly-config.md
  - https://github.com/earthly/earthly/blob/main/docs/earthly-command/earthly-command.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthly config file and the earthly config command

Goal: set global or git settings for earthly.

## File
Earthly reads `~/.earthly/config.yml` by default; override with `--config <path>` or `EARTHLY_CONFIG=<path>`. Shape:
```yaml
global:
    cache_size_mb: 20000
git:
    global:
        url_instead_of: "git@example.com:=https://localmirror.example.com/"
    github.com:
        auth: https
        user: alice
        password: itsasecret
```

## earthly config
`earthly [options] config [key] [value]` changes values in `~/.earthly/config.yml`, trying to preserve formatting and comments. `[value]` must be a valid YAML literal for the key.
- `--dry-run`: print the changed config to the console instead of writing it.

```
earthly config global.cache_size_mb 1234
earthly config global.buildkit_additional_args ['userns', '--host']
earthly config git."example.com".password hunter2
earthly config 'global.container_frontend' 'podman-shell'
```
Whole git server in one single-line YAML literal:
```
config git "{example: {pattern: 'example.com/([^/]+)', substitute: 'ssh://git@example.com:2222/var/git/repos/\$1.git', auth: ssh, user: git}}"
```
which yields a `git:` block with `example:` containing `pattern`, `substitute`, `auth: ssh` and `user: git`.

## Gotcha
A key containing a period is written with quotes around that part, as in `git."example.com".password`.

## Related settings
The `git` section holds per-site entries (`auth`, `user`, `password`) and a `global` entry with `url_instead_of`. The `global` section holds `cache_size_mb` (BuildKit cache size in MB; 0 or omitted means the BuildKit default of 10% of the root filesystem). Container frontend can be set with `earthly config 'global.container_frontend' 'docker-shell'` for Docker.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthly-config/earthly-config.md, earthly-command/earthly-command.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.

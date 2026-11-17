---
id: computing-software.systems-network-administration.navidrome.navidrome-cli-reference-and-docker
name: navidrome-cli-reference-and-docker
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, cli, navidrome-command, docker-compose-run, global-flags, configfile, nobanner, subcommands]
level: practitioner
status: docs-checked
description: "Use the Navidrome command line: command list, global flags, running commands against the same config as the server, and the Docker Compose run versus exec patterns."
sources: ["https://www.navidrome.org/docs/usage/admin/cli/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome CLI reference

`navidrome` with no command starts the server. `navidrome --help` and `navidrome <command> [<subcommand>] --help` show flags for your version.

Commands: `artwork`, `backup`, `doctor`, `inspect`, `missing`, `plugin`, `pls`, `scan`, `search`, `service`, `user`.

Global flags: `-c/--configfile` (default `./navidrome.toml`), `-n/--nobanner`, `--musicfolder`, `--datafolder` (needs write access), `--cachefolder` (needs write access), `-l/--loglevel` (`error`, `info`, `debug`, `trace`), `--logfile`.

Commands read the same config file and `ND_` variables as the server. Run them with the same settings or they act on a different database. In scripts always pass `--configfile`:

```bash
navidrome -c /etc/navidrome/navidrome.toml --nobanner user list
```

Docker Compose:

```bash
docker compose run --rm navidrome --help
docker compose run --rm navidrome scan --full
docker compose exec navidrome navidrome user list   # inside the running container
```
`docker run --rm -it ... navidrome/navidrome:latest user list` works too; use the same image tag, volumes, `--env-file` and `ND_CONFIGFILE`. `-it` is required for prompts such as the password in `user create`.

Safety notes from the reference: stop Navidrome before `backup restore` or `search rebuild`; `backup restore`, `backup prune` and `missing fix` cannot be undone, so run `navidrome backup create` first and double-check paths and IDs.

## Checked

2026-11-04. Confirmed against the Navidrome Command-Line Interface page: command list, global flags and defaults, shared config, Docker Compose run and exec, docker run with `-it`, and the safety notes. Nothing removed.

Method: documentation only; no commands were run.

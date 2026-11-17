---
id: computing-software.devops-ci-cd.gitea.windows-service
name: windows-service
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-windows-service, gitea, sc-exe, delayed-auto, windows-run-user, absolute-sqlite-path]
level: practitioner
status: docs-checked
description: "Register Gitea as a Windows service with sc.exe, set RUN_USER and absolute SQLite path, use delayed-auto start and database dependencies."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/installation/windows-service.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Registering Gitea as a Windows service

## Prerequisites in `<gitea-dir>\custom\conf\app.ini`
```ini
RUN_USER = COMPUTERNAME$
[database]
PATH = <gitea-dir>/data/gitea.db
```
`RUN_USER` runs Gitea as the local system user; `COMPUTERNAME` is the output of `echo %COMPUTERNAME%` (for `USER-PC` write `USER-PC$`). With SQLite3 use a full absolute `PATH`.

## Register (elevated cmd)
```sh
sc.exe create gitea start= auto binPath= "\"<gitea-dir>\gitea.exe\" web --config \"<gitea-dir>\custom\conf\app.ini\""
```
Replace `<gitea-dir>` with your directory. The space after `start=` and `binPath=` is part of sc.exe syntax. Start it from the Windows Services app; Gitea should answer on `http://localhost:3000` or the configured port.

## Startup problems
- On loaded systems the service can time out at boot (see the Windows Event Log). Use delayed start: `sc.exe config gitea start= delayed-auto` (or set it at creation).
- Wait for the database service: `sc.exe config gitea depend= mariadb` so a reboot postpones Gitea until the DB is ready.

## Remove
`sc.exe delete gitea` from an elevated prompt.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.

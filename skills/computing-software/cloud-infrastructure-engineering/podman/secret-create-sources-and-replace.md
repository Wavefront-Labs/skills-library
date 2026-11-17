---
id: computing-software.cloud-infrastructure-engineering.podman.secret-create-sources-and-replace
name: secret-create-sources-and-replace
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [secret-create, secrets, stdin, env, replace, ignore, podman-run-secret]
level: practitioner
status: docs-checked
description: "Create Podman secrets from a file, stdin or environment variable, use --replace and --ignore, attach labels, size limit, and mount them with podman run --secret."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-secret-create.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: store sensitive data outside images and source control.

`podman secret create [options] name file|-` reads the secret from a file path or from stdin with `-`. A secret is sensitive data a container needs at runtime, up to 512 kB. Secrets are not committed with `podman commit` nor included in `podman export` archives, and can store passwords for `podman login`.

Sources: `echo -n mysecret > ./secret.txt` then `podman secret create my_secret ./secret.txt`; `printf <secret> | podman secret create my_secret -`; `podman secret create --env=true my_secret MYSECRET` reads from the environment variable `MYSECRET`.

Rotation: `--replace` updates an existing secret but changes only newly created containers, not existing ones; `--ignore` returns the existing secret's ID instead of an error; they cannot be combined. Example from the page: `openssl rand -base64 378000 | podman secret create --replace my_secret -`, just under the 512000 byte maximum.

`--label`/`-l` adds metadata shown by `podman secret inspect` and `ls`. `--driver`/`-d` sets the driver (default `file`); `--driver-opts` passes driver options.

Use in a container: `podman run --rm --secret source=my_secret,type=mount,uid=1001,gid=1001,mode=440 docker.io/library/alpine ls -l /run/secrets/my_secret`.

## Checked
2026-11-09: read the podman-secret-create man page in full and confirmed the 512 kB limit, commit and export behaviour, the file, stdin and env sources, --replace and --ignore semantics, --label, --driver default and --driver-opts, the rotation example and the run example. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.


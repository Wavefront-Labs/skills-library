---
id: computing-software.cloud-infrastructure-engineering.podman.secret-drivers-file-pass-shell
name: secret-drivers-file-pass-shell
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [secret-drivers, file-driver, pass-driver, shell-driver, secret-id, containers-conf, gpg]
level: advanced
status: docs-checked
description: "Choose a Podman secret driver: file, pass (GPG-encrypted), or shell with custom list, lookup, store and delete scripts configured in containers.conf."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-secret-create.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: select where secret data is stored.

`podman secret create --driver` (`-d`) defaults to `file`. The three drivers described:

- `file`: the secret resides in a read-protected file.
- `pass`: the secret resides in a GPG-encrypted file. Example: `podman secret create --driver=pass my_secret ./secret.txt.gpg`.
- `shell`: secrets are managed by custom scripts. The environment variable `SECRET_ID` is passed to the scripts (except for `list`), and secrets are communicated over stdin/stdout where applicable. Four driver options install the scripts: `list`, `lookup`, `store` and `delete`.

The shell driver is configured in containers.conf:

```
[secrets]
driver = "shell"
[secrets.opts]
list =
lookup =
store =
delete =
```

Use `--driver-opts key1=val1,key2=val2` for driver-specific options on the command line. Whatever the driver, a secret you create is mounted or exposed to containers with `podman run --secret`.


Secrets can also hold passwords for `podman login`, so the driver choice affects where registry passwords live. The page documents only the driver names `file`, `pass` and `shell`.

## Checked

2026-11-09. Read against the official page text (podman-secret-create.1); drivers, the default, SECRET_ID, the shell options and the pass example were confirmed there. Nothing removed.
Method: documentation only; no commands were run.

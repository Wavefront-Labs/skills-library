---
id: computing-software.systems-network-administration.linux.podman-secrets
name: podman-secrets
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, podman-secrets, podman-secret, quadlet-secret, container-secrets, secret-driver, pass-driver]
level: practitioner
status: docs-checked
description: "Manage container secrets with podman secret: create, mount as files or env vars, drivers (file, pass, shell), use in Quadlet units and kube play, and rotation without leaks."
sources:
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-secret-create.1.md
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-secret-inspect.1.md
  - https://github.com/containers/podman/blob/main/docs/source/markdown/options/secret.md
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-systemd.unit.5.md
  - https://github.com/containers/podman/blob/main/docs/source/markdown/podman-kube-play.1.md.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Secrets with podman secret

Secrets keep credentials out of images, `podman inspect` output and shell history-baked env vars.

## Create
```bash
printf '%s' 's3cr3t' | podman secret create db_password -        # from stdin; avoid echo with trailing newline
podman secret create tls_key ./server.key
podman secret create --env=true api_token API_TOKEN               # from an environment variable
podman secret ls; podman secret inspect db_password                # metadata only
podman secret inspect --showsecret db_password                     # prints the value; guard access
```
Secrets are limited to 512 kB and are not committed by `podman commit` or included in `podman export`.

## Use
```bash
podman run --secret db_password app                         # mounted as the file /run/secrets/db_password
podman run --secret db_password,type=env,target=DB_PASSWORD app
podman run --secret tls_key,target=/etc/app/tls.key,mode=0400,uid=1000 app   # uid/gid/mode apply to mounts only (defaults 0, 0, 0444)
```
Prefer file mounts: environment variables are inherited by child processes and tend to show up in diagnostics. Many images accept `*_FILE` variables that point at a mounted secret path; check the image's documentation.

## Drivers
- `file` (default): the secret resides in a read-protected file.
- `pass`: the secret resides in a GPG-encrypted file (`--driver=pass`, optional `--driver-opts`).
- `shell`: custom scripts manage the secret; `list`, `lookup`, `store` and `delete` driver options install them, `SECRET_ID` is passed in the environment and values travel via stdin/stdout.
The `containers.conf` `[secrets]` table sets the driver (`driver = "shell"` with `[secrets.opts]` for the scripts).

## Quadlet and systemd
```ini
# ~/.config/containers/systemd/app.container
[Container]
Image=registry.example.com/app:1.4
Secret=db_password,type=env,target=DB_PASSWORD
Secret=tls_key,target=/etc/app/tls.key,mode=0400
```
## kube play
A Kubernetes `Secret` in the YAML given to `podman kube play app.yaml` is saved as a Podman named secret that Pods can reference for environment variables or volumes. (`--replace` tears down and recreates the pods; it is not documented as updating secrets.)

## Rotation
`--replace` updates an existing secret of the same name, but it does not change secrets inside existing containers, only newly created ones, so recreate the containers.
```bash
printf '%s' 'n3w' | podman secret create --replace db_password -
systemctl --user restart app.service                                # recreate/restart so the new value is picked up
```

## Verify
- [ ] `podman inspect app | grep -i s3cr3t` returns nothing; `podman exec app cat /run/secrets/db_password` works.
- [ ] The image history has no credentials (`podman history --no-trunc`).

## Checked
Checked 2026-10-25 against the Podman documentation source on GitHub (containers/podman docs/, main, last commit 2026-10-23; latest release v5.8.9 of 2026-10-12): `podman secret create` (name plus file or `-`, `--driver`, `--driver-opts`, `--env`, `--replace`, `--ignore`, `--label`), drivers file/pass/shell, the 512 kB limit, `podman secret inspect --showsecret`, `--secret` options `type=mount|env`, `target`, `uid`, `gid`, `mode` (default 0444) and the `/run/secrets/<name>` default path, Quadlet `Secret=` key, kube play Secret objects becoming Podman secrets, `--replace` semantics. Removed unconfirmed claims: version gates for `--showsecret` and `--replace`, the file driver's storage format, `/proc/<pid>/environ` remark and per-user secret scoping.

Method: documentation only; no commands were run.

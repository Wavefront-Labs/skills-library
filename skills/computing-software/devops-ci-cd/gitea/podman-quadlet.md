---
id: computing-software.devops-ci-cd.gitea.podman-quadlet
name: podman-quadlet
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-quadlet, gitea, podman-quadlet, gitea-quadlets-file, loginctl-enable-linger, rootless-quadlet]
level: practitioner
status: docs-checked
description: "Deploy Gitea with Podman Quadlet: one gitea.quadlets file, volumes, rootless image, podman quadlet install, PostgreSQL network, linger and journalctl."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/installation/with-podman-quadlet.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea with Podman Quadlet

Rootless quadlets install into `~/.config/containers/systemd/` and use the rootless image; a rootful directory such as `/etc/containers/systemd/` should use the rootful image. Since Podman v6.0 one `gitea.quadlets` file may hold several quadlets separated by `---`, each with a `# FileName=` comment.

```ini
# FileName=gitea-data
[Volume]
VolumeName=gitea-data
---
# FileName=gitea-config
[Volume]
VolumeName=gitea-config
---
# FileName=gitea
[Container]
PublishPort=2222:2222
PublishPort=3000:3000
Image=docker.gitea.com/gitea:<version>-rootless
ContainerName=gitea
Mount=type=volume,src=gitea-data.volume,destination=/var/lib/gitea
Mount=type=volume,src=gitea-config.volume,destination=/etc/gitea

[Service]
Restart=always

[Install]
WantedBy=default.target
```
Install and inspect:
```sh
podman quadlet install ./gitea.quadlets --application=gitea
podman quadlet list
systemctl --user start gitea
```
`--application=gitea` groups the generated files in a `gitea/` subdirectory. Freshly installed `gitea.container` may show `failed/failed` until started.

`WantedBy=default.target` starts it with the user session; rootless user services do not run without a session, so for start at boot run `loginctl enable-linger $USER`.

## PostgreSQL
Add a `[Network]` quadlet (`NetworkName=gitea`), a postgres volume, a `gitea-postgres` container (`Image=docker.io/library/postgres:18`, `Network=gitea.network`, `Environment=POSTGRES_USER/PASSWORD/DB`, mount at `/var/lib/postgresql`), and in the gitea quadlet add `[Unit] Requires=gitea-postgres.service` plus `After=gitea-postgres.service`, `Network=gitea.network` and `Environment=GITEA__database__DB_TYPE=postgres`, `GITEA__database__HOST=gitea-postgres:5432`, `NAME`, `USER`, `PASSWD`.

## Logs
`journalctl --user --follow --unit=gitea.service` (systemd manages the container).

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.

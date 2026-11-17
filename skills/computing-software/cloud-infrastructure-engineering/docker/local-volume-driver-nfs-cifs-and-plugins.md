---
id: computing-software.cloud-infrastructure-engineering.docker.local-volume-driver-nfs-cifs-and-plugins
name: local-volume-driver-nfs-cifs-and-plugins
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, volume-driver, volume-drivers, nfs-volume, local-driver-nfs, nfs-opts, cifs-volume, smb-volume, local-driver-o, volume-bind-o, volume-plugin, plugin-enable, plugin-upgrade]
level: advanced
description: "Mount NFS and SMB shares, tmpfs and bind paths as named volumes via the local driver's type/o/device options, and manage volume plugins through their lifecycle."
sources: ["https://docs.docker.com/engine/storage/volumes/", "https://docs.docker.com/reference/cli/docker/volume/create/", "https://docs.docker.com/reference/cli/docker/plugin/install/", "https://docs.docker.com/reference/cli/docker/plugin/upgrade/", "https://docs.docker.com/reference/cli/docker/plugin/disable/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Local volume driver: NFS, CIFS, -o options and plugins

The `local` driver accepts `type`, `o` and `device` options (`--opt`) that describe a
filesystem to mount, such as an NFS export or a CIFS share.

## NFS
```sh
docker volume create --driver local \
  --opt type=nfs --opt o=addr=10.0.0.10,rw,nfsvers=4 \
  --opt device=:/exports/app nfs-app
```
```yaml
volumes:
  nfs-app:
    driver_opts:
      type: nfs
      o: "addr=10.0.0.10,rw,nfsvers=4"
      device: ":/exports/app"
```
- `device` starts with `:` when the server address is given in `addr=` (as in the Docker
  docs NFS example, `device=:/var/docker-nfs`).
- Other NFS mount options appear in the docs examples, for example `vers=4,soft,timeo=180` and
  `nfsvers=4,async`; quote an `o=` value that contains commas when using `--mount`.

## CIFS/SMB
```sh
docker volume create --driver local \
  --opt type=cifs --opt device=//fileserver/share \
  --opt o=addr=fileserver,username=svc,password=$SMB_PASS,file_mode=0640,dir_mode=0750 \
  --name smb-share
```
`addr` is required when `device` uses a hostname instead of an IP, so Docker can perform the
lookup. Volume options are stored with the volume, so treat any password passed this way as
visible to anyone who can inspect it.

## tmpfs and bind via -o
```sh
docker volume create --opt type=tmpfs --opt device=tmpfs --opt o=size=256m,uid=1000 scratch
docker volume create --opt type=none --opt o=bind --opt device=/srv/data appdata   # named volume backed by a host dir
```
The bind form gives a stable volume name while data lives at a chosen host path; create the
directory first.

## Plugins
```sh
docker plugin install --alias sshfs vieux/sshfs DEBUG=1 --grant-all-permissions
docker plugin ls
docker volume create -d sshfs -o sshcmd=user@host:/path -o password=... sshvol
docker plugin disable sshfs        # -f / --force disables an active plugin
docker plugin upgrade sshfs vieux/sshfs:next --grant-all-permissions   # plugin must be disabled first
docker plugin enable sshfs
docker plugin rm sshfs
```
Plugins request privileges at install; review them before granting (`--grant-all-permissions`
accepts all of them). `docker plugin rm -f` is not recommended because it can affect
running containers.

## Verify
`docker run --rm -v nfs-app:/d alpine sh -c 'touch /d/x && ls -l /d'`.

## Checked

Date: 2026-10-24. Documentation release: Docker Engine storage docs and Docker CLI references (docker/docs and docker/cli main).
Confirmed: local driver `type`/`o`/`device` options, the NFS `device=:/path` plus `addr=` form, CIFS options
and the `addr` requirement for hostnames, `docker plugin install --alias --grant-all-permissions`, `plugin disable -f`,
`plugin upgrade` requiring a disabled plugin, and the `plugin rm --force` caution. Removed: the host package
names, Swarm behaviour, `hard,timeo` NFS options and `nfsvers=4.1` (not in the docs; docs use `nfsvers=4`/`vers=4`),
the `credentials=` file advice, and the claim about unmaintained legacy plugins. The tmpfs and bind `-o` volume forms follow the `docker volume create` option documentation.

Method: documentation only; no commands were run.

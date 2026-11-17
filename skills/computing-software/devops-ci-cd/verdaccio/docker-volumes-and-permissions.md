---
id: computing-software.devops-ci-cd.verdaccio.docker-volumes-and-permissions
name: docker-volumes-and-permissions
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [docker-volume, bind-mount, uid-10001, chown, named-volume, selinux]
level: practitioner
status: docs-checked
description: "Persist Verdaccio config, storage and plugins in Docker with bind mounts or volumes, fix uid 10001 permission errors and SELinux relabeling."
sources:
  - https://verdaccio.org/docs/docker/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```
V_PATH=/path/for/verdaccio; docker run -it --rm --name verdaccio -p 4873:4873 \
  -v $V_PATH/conf:/verdaccio/conf \
  -v $V_PATH/storage:/verdaccio/storage \
  -v $V_PATH/plugins:/verdaccio/plugins \
  verdaccio/verdaccio
```
You must put a `config.yaml` in the mounted conf folder first (start from the repo's `docker.yaml`); the container will not start properly without it. Lock the file down for production.

Permissions: the process runs as uid 10001. For bind mounts:
```
sudo chown -R 10001:65533 /path/for/verdaccio
```
Named Docker volumes are recommended over bind mounts.

SELinux: the symptom is `cannot open config file /verdaccio/conf/config.yaml ... does not look like a valid config file`, confirmed by an AVC denial in the audit log. Fix:
```
chcon -Rt container_file_t ./conf
```
or add `:z` (shared) or `:Z` (private to this container) to the mount; use these flags carefully as they relabel the directory.

Kubernetes note: the same storage path appears in the Helm configMap (see helm skill).

Verify: restart the container and confirm published packages persist.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Docker. Confirmed: the bind-mount example, the required config.yaml, uid 10001 and chown 10001:65533, named volumes preferred, the SELinux error, chcon, :z and :Z, and the Helm storage path on the Kubernetes page. Removed or corrected: nothing.

Method: documentation only; no commands were run.

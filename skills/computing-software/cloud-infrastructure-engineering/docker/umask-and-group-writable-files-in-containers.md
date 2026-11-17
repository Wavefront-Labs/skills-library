---
id: computing-software.cloud-infrastructure-engineering.docker.umask-and-group-writable-files-in-containers
name: umask-and-group-writable-files-in-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, file-permissions, umask, setgid, shared-volume, group-add, entrypoint-script]
level: practitioner
status: docs-checked
description: "Make files on shared volumes editable across containers and host users: umask in entrypoints, setgid dirs, shared GIDs via --group-add, app UMASK settings."
sources: ["https://man7.org/linux/man-pages/man2/umask.2.html", "https://docs.docker.com/reference/cli/docker/container/run/#group-add", "https://docs.linuxserver.io/general/understanding-puid-and-pgid/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# umask and group-writable files in containers

The typical default process umask is `022`: new files are `644`, dirs `755` (umask(2)). When two
containers (or a container and a host user) share a volume under different UIDs, the second
one can read but not modify the first one's files.

## Recipe: shared group + umask 002 + setgid dir
```bash
# host or init step: shared dir owned by a common group, setgid so new files inherit it
sudo groupadd -g 2000 shared
sudo install -d -o root -g 2000 -m 2775 /srv/shared
```
```sh
#!/bin/sh
# entrypoint.sh in each image that writes there
umask 0002
exec "$@"
```
```bash
docker run -d --user 1001:1001 --group-add 2000 -v /srv/shared:/shared writer:1.0
docker run -d --user 1002:1002 --group-add 2000 -v /srv/shared:/shared reader-editor:1.0
```
Result: files created `664`, dirs `775`, group `2000` on everything; both containers edit
each other's files.

Set umask in the entrypoint, the app config, or the supervisor.

Applications usually have their own umask setting; check the application's documentation.

## Dockerfile note

## Verify
```bash
docker exec <c> sh -c 'umask; touch /shared/t; ls -ln /shared/t'   # 0002, -rw-rw-r-- 1001 2000
stat -c '%a %U:%G' /srv/shared                                       # 2775
```

## Checked
2026-10-31. Confirmed in umask(2): typical default 022 (0666 becomes 0644), inheritance across fork, unchanged by execve, default ACL overrides umask; Docker run reference lists `--group-add`. Removed: no-`--umask` claim, application umask table (linuxserver page too thin to confirm), Dockerfile RUN note, squash and open(0600) gotchas.
Method: documentation only; no commands were run.

## Gotchas
- A child process inherits its parent's umask, and `execve` leaves it unchanged.
- Per umask(2), a default ACL on the parent directory makes the umask ignored: the default
  ACL is inherited instead.

---
id: computing-software.cloud-infrastructure-engineering.docker.matching-host-uids-entrypoint-chown-and-shared-dirs
name: matching-host-uids-entrypoint-chown-and-shared-dirs
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, mount-permissions, file-permissions, uid-mapping, uid-build-arg, match-host-uid, entrypoint-chown, fix-perms, setgid, acl]
level: practitioner
description: "Fix bind-mount permission errors on Linux hosts by matching the host UID, chowning in the entrypoint, or using setgid directories and default ACLs for multi-service writes."
sources: ["https://docs.docker.com/engine/storage/bind-mounts/", "https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user", "https://man7.org/linux/man-pages/man1/setfacl.1.html", "https://man7.org/linux/man-pages/man7/inode.7.html", "https://man7.org/linux/man-pages/man1/chmod.1p.html", "https://docs.docker.com/reference/cli/docker/container/run/", "https://docs.docker.com/reference/cli/docker/buildx/build/", "https://docs.docker.com/engine/storage/volumes/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Matching host UIDs, entrypoint chown and shared directories

On Docker CE/EE on Linux, files in a bind mount have the exact same permissions inside the
container as outside, including owner UID and GID; the user and group names do not matter.
So the container user needs the same UID, or to be in a group with the same GID. Docker
Desktop behaves differently: on Mac, mounted files act as if owned by the container user
(local operations use your local user's permissions); on Windows, they appear owned by root but
the specified user can still read and write them. The rest of this skill is about the Linux case.

## Option 1 - build the image with the host's UID (dev images)
```dockerfile
ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
USER $USERNAME
```
```sh
docker build --build-arg USER_UID=$(id -u) --build-arg USER_GID=$(id -g) -t app:dev .
```
This is the VS Code Dev Containers snippet. If the build fails because the UID or GID already
exists, the base image already has a non-root user you can use instead. The image is now
host-specific: fine for dev, not for registries. To change the UID/GID of an existing user in
the image, the same page gives `groupmod --gid`, `usermod --uid ... --gid ...` and
`chown -R $USER_UID:$USER_GID` on the user's home directory (on Alpine, install the `shadow` package first).

Runtime alternative: `docker run --user $(id -u):$(id -g)` (`-u, --user` takes
`<name|uid>[:<group|gid>]`). In Compose, a service takes `user: user-name-or-UID`. In a
devcontainer, `remoteUser` makes VS Code use the user, and on Linux it also updates the
container user's UID/GID to match your local user unless `"updateRemoteUserUID": false`;
the update is applied when the container is created, so changing it needs a rebuild.

## Option 2 - fix ownership at startup
Start the entrypoint as root, `chown -R <uid>:<gid> /data` the mount if the owner is wrong,
then drop to the unprivileged user before running the app (use a privilege-dropping tool of
your choice; none is covered by the cited pages). Costs: a recursive chown is slow on big
trees and changes ownership of the files on the host.

## Option 3 - shared directory with setgid + ACLs (several writers)
```sh
sudo groupadd --gid 2000 appshare
sudo chown -R <owner-uid>:2000 /srv/shared && sudo chmod -R 2775 /srv/shared   # 2000 bit = set-group-ID
sudo setfacl -R -m g:appshare:rwX /srv/shared
sudo setfacl -R -d -m g:appshare:rwX /srv/shared                          # -d: default ACL
docker run --group-add 2000 -v /srv/shared:/shared app:1
```
On a directory the set-group-ID bit makes files created there inherit the directory's group
rather than the creator's effective group, and new subdirectories get the bit too. `-d` makes
the operations apply to the Default ACL, `-R` applies them recursively, and `X` means execute
only if the target is a directory or already executable for someone. `--group-add` adds an
additional group for the container's process, so every container can join GID 2000 whatever
its own UID. Check that the application's umask does not strip group write; that is not covered
by the cited pages.

## Choosing
| Situation | Use |
|---|---|
| Local dev bind mounting source | Option 1 or `--user $(id -u)` |
| Production volume pre-owned by root | Option 2, once |
| Multiple services/UIDs writing one dir | Option 3 |
| Avoid bind mounts | a named volume: a new volume is pre-populated with the image's directory contents (the volumes page does not discuss ownership) |

## Checked
Date: 2026-11-07
Pages read in full: Docker bind mounts, VS Code "Add a non-root user to a container", setfacl(1) (read the
description, options and ACL entries sections; the later sections on mask/examples were not read), inode(7)
set-group-ID paragraph (searched, not whole page), chmod(1p) (octal table and `-R` searched, not whole page).
docker container run and docker buildx build pages: option rows only (`-u/--user`, `--group-add`, `--build-arg`);
volumes page: the pre-populate paragraphs only.
Corrections: "Bind mounts pass UIDs unchanged" was only true for Linux Docker CE/EE; Docker Desktop on
Mac and Windows maps ownership differently (added). Removed: the `EACCES` error name, `useradd -l`, the
`$UID` export remark and the Compose `build.args` line, the `stat -c`, `setpriv`, `gosu` and `usermod -u`
snippets (none on a cited page), the `umask 002` value, the "initialised from image ownership" claim for named
volumes, `chgrp` (replaced by `chown`), and the invented Verify step with expected output. Not confirmed on
any page and therefore not included: the compose `UID` variable behaviour.
Method: documentation only; no commands were run.

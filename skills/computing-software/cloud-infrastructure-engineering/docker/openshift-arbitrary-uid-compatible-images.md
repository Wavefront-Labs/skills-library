---
id: computing-software.cloud-infrastructure-engineering.docker.openshift-arbitrary-uid-compatible-images
name: openshift-arbitrary-uid-compatible-images
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, non-root, arbitrary-uid, openshift-uid, group-zero, restricted-scc, file-permissions]
level: advanced
status: docs-checked
description: "Build images that run under OpenShift's random UID: group 0 ownership with g=u permissions, no reliance on /etc/passwd entries, HOME handling and nss_wrapper."
sources: ["https://docs.openshift.com/container-platform/latest/openshift_images/create-images.html", "https://docs.openshift.com/container-platform/latest/authentication/managing-security-context-constraints.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Images that run with an arbitrary UID (OpenShift)

OpenShift's default `restricted-v2` SCC assigns the container a user ID from the namespace's range
instead of the one your image names, and the container user is always a member of the **root group
(GID 0)**. The SCC docs: a pod that requests a specific user ID is only accepted if an SCC allows
that ID. Files owned by your image's `app` user can therefore become unwritable.

## Recipe
From the OpenShift "Support arbitrary user ids" guidance: directories and files that processes in
the image write to must be owned by the root group and be read/writable by that group; files to be
executed also need group execute permission.
```dockerfile
FROM <base-image>
WORKDIR /opt/app
COPY --chown=1001:0 . /opt/app
RUN mkdir -p /opt/app/data /opt/app/tmp \
 && chgrp -R 0 /opt/app \
 && chmod -R g=u /opt/app          # group gets the same rights as the owner
ENV HOME=/opt/app
USER 1001                          # numeric
```
Key idea: ownership by **group 0** plus group permissions equal to user permissions. Any
user in group 0 can then read/write what the image intends to be writable.

## Things that break and fixes
| Symptom | Cause | Fix |
|---|---|---|
| `Permission denied` writing to app dir | Owned by uid 1001 with no group write | `chgrp -R 0` + `chmod -R g=u` on the writable paths |
| Tools need a writable home directory | HOME not pointing at a group-0 writable path | `ENV HOME=/opt/app` (writable by group 0) |
| Binds to port 80 fail | `restricted-v2` drops all capabilities and the process is non-root | Listen on a high port such as 8080 |

## /etc/passwd
Do not make `/etc/passwd` group-writable. The OpenShift docs warn that loosening permissions on
sensitive files such as `/etc/passwd` can let unintended users modify them, and say CRI-O
supports inserting arbitrary user IDs into a container's `/etc/passwd`, so changing permissions is
never required. They also say `/etc/passwd` should not exist in the image, otherwise CRI-O fails to
inject the random UID and the container may have trouble resolving its UID. Check the current
page for this requirement against your base image.

## Test without a cluster
```bash
docker run --rm --user 1000680000:0 <image>           # arbitrary UID, group 0
docker run --rm --user 1000680000:0 --read-only --tmpfs /tmp <image>
```
This approximates the permission model; confirm in a real project as well.

## Gotchas
- Do not `chmod 777`; group 0 ownership with `g=u` is the documented approach.
- The SCC `fsGroup` and `supplementalGroups` strategies take their ranges from the namespace
  annotations (`openshift.io/sa.scc.supplemental-groups`, falling back to
  `openshift.io/sa.scc.uid-range`); use `fsGroup` for volume ownership instead of chowning at start.

## Checked
Checked 2026-10-28 against OpenShift Container Platform docs "Creating images" (support arbitrary
user ids, `chgrp -R 0` and `chmod -R g=u`, `/etc/passwd` guidance) and "Managing security context
constraints" (`restricted-v2` drops ALL capabilities, requested user IDs, fsGroup and
supplementalGroups annotations). Corrected: the earlier append-to-`/etc/passwd` entrypoint and the
group-writable passwd advice contradicted the docs. Removed as unconfirmed: the UBI image name, the
example UID claim, nss_wrapper, the HOME-defaults-to-`/` claim, and the setuid/`gosu` remark.
Method: documentation only; no commands were run.

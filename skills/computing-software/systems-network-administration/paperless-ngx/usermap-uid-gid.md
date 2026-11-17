---
id: computing-software.systems-network-administration.paperless-ngx.usermap-uid-gid
name: usermap-uid-gid
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, usermap-uid, usermap-gid, rootless, permission-denied, docker]
level: practitioner
status: docs-checked
description: "Fix consume and export permission errors by setting USERMAP_UID and USERMAP_GID, or run the container rootless with a compose user entry."
sources:
  - "https://docs.paperless-ngx.com/setup/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/troubleshooting/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matching container and host users

## The default approach
`USERMAP_UID` is the ID of the paperless user in the container and `USERMAP_GID` the ID of its group; both default to 1000. Set them (in `docker-compose.env`) to your actual host user and group IDs:
```bash
id -u
id -g
```
Paperless changes ownership on its folders to this user, so the values must be right for you to write to the consumption directory. If your UID and GID are already 1000, this usually works without changes.

## Symptoms of a mismatch
- `[Errno 13] Permission denied` when paperless cannot delete a file inside the consumption directory. The page says to set USERMAP_UID and USERMAP_GID to your host IDs if they differ from 1000, and to ensure you can read and write the consumption directory on the host.
- `chown: changing ownership of '../export': Operation not permitted`. The container tries to set ownership on the listed directories so the paperless user has write access. This happens, for example, when those directories point to NFS shares. Ensure that `chown` is possible on them.

## Rootless alternative
Set `user:` in `docker-compose.yml` to the UID and GID of your host user. The container process starts directly as that user with no internal privilege remapping, and any UID and GID is supported:
```yaml
webserver:
  image: ghcr.io/paperless-ngx/paperless-ngx:latest
  user: '1000:1000'
```
- Do not combine this with `USERMAP_UID` or `USERMAP_GID`.
- It is not possible to run rootless if additional languages are specified via `PAPERLESS_OCR_LANGUAGES`.

## Checked
Date: 2026-11-07
Pages read in full: none in full. I read the relevant sections of setup (Docker Compose step 3 and the rootless section), configuration (USERMAP_UID and USERMAP_GID entries) and troubleshooting (Operation not permitted; Permission denied in the consumption directory).
Corrections: removed "Inside the container, Paperless runs as a user whose IDs default to 1000:1000" in favour of the configuration wording; added the 1000 shortcut from setup; removed the "fails on some network shares such as NFS" generalisation to the page's "for example" wording; added the image line from the setup example.
Method: documentation only; no commands were run.

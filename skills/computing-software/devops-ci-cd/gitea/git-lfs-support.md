---
id: computing-software.devops-ci-cd.gitea.git-lfs-support
name: git-lfs-support
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-lfs-jwt, gitea, lfs-start-server, lfs-allow-pure-ssh, git-lfs, lfs-pointer-sha, lfs-ssh-automultiplex]
level: practitioner
status: docs-checked
description: "Enable built-in Git LFS in Gitea, the pure SSH protocol option and its client workaround, and the sha rule when changing LFS files via the contents API."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/administration/git-lfs-support.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Git LFS in Gitea

```ini
[server]
LFS_START_SERVER = true     ; default false

[lfs]
PATH = <gitea-home>/data/lfs ; default data/lfs
```
The server needs Git >= 2.1.2.

## Pure SSH protocol
`[server] LFS_ALLOW_PURE_SSH = true` lets LFS run purely over SSH without exposing an HTTP endpoint. It defaults to false because of an open git-lfs client bug that makes SSH transfers hang; work around on every client with `git config --global lfs.ssh.automultiplex false`.

## Changing LFS files through the contents API
`PUT`/`DELETE /repos/{owner}/{repo}/contents/{filepath}` and `POST /repos/{owner}/{repo}/contents` store content as an LFS object and commit a pointer if the path matches a `filter=lfs` rule in `.gitattributes`. For an existing file the required `sha` is the ID of the **pointer blob**: take `sha` from `GET /repos/{owner}/{repo}/contents/{filepath}`. Do not send `lfs_oid` or a checksum of the content, or you get `sha does not match` although the request looks right.

Secrets: the LFS JWT signing secret is `JWT_SECRET` (`gitea generate secret JWT_SECRET`).

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.

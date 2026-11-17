---
id: computing-software.systems-network-administration.syncthing.folder-type-receive-only
name: folder-type-receive-only
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, folder-types, receive-only, revert]
level: practitioner
status: docs-checked
description: "Run a Syncthing receive only folder for mirrors and backups and revert local changes in the GUI or with POST /rest/db/revert."
sources: ["https://docs.syncthing.net/users/foldertypes.html", "https://docs.syncthing.net/rest/db-revert-post.html", "https://docs.syncthing.net/rest/db-localchanged-get.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Receive only folders

## Behaviour
Added in version 0.14.50. In a receive only folder all changes from the cluster are applied and redistributed to other devices, as in the default send-receive mode, but local changes are not distributed. The docs call it useful for replication mirrors, backup destinations, or cases where no local modifications are expected or allowed.

As with send-receive, local modifications are preserved and do not make the folder out of sync. The device will however look out of sync on other devices, as it no longer has the latest/expected version of the modified file.

## Reverting
The GUI shows a red Revert Local Changes button when local changes exist. Using it undoes them: added files are deleted, and modified or deleted files are fetched again.

```sh
curl -X POST -H "X-API-Key: <key>" "http://127.0.0.1:8384/rest/db/revert?folder=default"
```
`folder` is mandatory (added in 0.14.50) and the call does nothing if the folder is not receive only.

List the locally changed files with `GET /rest/db/localchanged?folder=default` (added in 0.14.55). `folder` is mandatory and results can be paginated with the common `page` and `perpage` parameters. The page notes it is an expensive call, increasing CPU and RAM usage, and to use it sparingly.

## Conflicts
A locally modified file that is subsequently modified by the cluster causes a sync conflict, resolved with the cluster version as the winner. The sync conflict copy is not sent to the cluster and is deleted if Revert Local Changes is used.

## Checked
2026-11-04. Read Folder Types and the REST pages for db/revert and db/localchanged: version notes, behaviour, revert button wording, mandatory `folder` parameter, no-op for other folder types, pagination, the expensive-call note and conflict handling. Reworded to the page text.
Method: documentation only; no commands were run.

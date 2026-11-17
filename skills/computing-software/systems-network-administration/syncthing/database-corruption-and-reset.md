---
id: computing-software.systems-network-administration.syncthing.database-corruption-and-reset
name: database-corruption-and-reset
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, database, index-reset, troubleshooting]
level: practitioner
status: docs-checked
description: "Recover from a corrupt Syncthing index database by deleting it or resetting through POST /rest/system/reset."
sources: ["https://docs.syncthing.net/users/faq.html", "https://docs.syncthing.net/rest/system-reset-post.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Corrupt or inconsistent index database

## Cause
The FAQ says a corrupt index database is almost always the result of bad RAM, a failing storage device or other hardware. Syncthing cannot operate, notes this in the logs and exits. Check the system, since faulty hardware may put it at risk of further data loss.

## Rebuild
Delete the database folder inside Syncthing's data directory and restart Syncthing. It then needs to perform a full re-hashing of all shared folders.

## Reset via REST
```sh
curl -X POST -H "X-API-Key: <key>" "http://127.0.0.1:8384/rest/system/reset"
curl -X POST -H "X-API-Key: <key>" "http://127.0.0.1:8384/rest/system/reset?folder=<id>"
```
Post with an empty body. Without parameters the entire database is erased from disk and Syncthing restarts. With `folder` set to a valid folder ID, only that folder's information is erased. It creates `.stfolder` folders in each sync folder if they do not already exist.

## Caution
Ensure that all sync folders which are mountpoints are already mounted. Inconsistent versions may result if the mountpoint is later mounted and contains older versions.

## Checked
2026-11-04. Read the FAQ entry on a corrupt database and the POST /rest/system/reset page: cause, delete-the-database-folder remedy, full re-hash, whole-database versus `folder` reset, restart, `.stfolder` creation and the mountpoint caution. Removed the `syncthing paths` hint, the claim that files are unaffected, and the Aftermath advice, none of which the pages state.
Method: documentation only; no commands were run.

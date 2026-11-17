---
id: computing-software.systems-network-administration.syncthing.folder-type-send-only
name: folder-type-send-only
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, folder-types, send-only, override]
level: practitioner
status: docs-checked
description: "Configure a Syncthing send only folder as a reference copy and use Override Changes or POST /rest/db/override to enforce it."
sources: ["https://docs.syncthing.net/users/foldertypes.html", "https://docs.syncthing.net/rest/db-override-post.html", "https://docs.syncthing.net/users/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Send only folders

## Purpose
A send only folder is intended for devices that keep a reference copy of files, where the files are not expected to change on other devices or such changes would be undesirable. All changes from other devices are ignored. Changes are still received, so the folder may become out of sync, but no changes are applied.

## Enforcing local state
When a send only folder becomes out of sync, the GUI shows a red Override Changes button at the bottom of the folder details. Clicking it enforces this host's current state on the rest of the cluster: changes made to files are overwritten by this host's version, and files that do not exist on this host are deleted.

The REST equivalent is:

```sh
curl -X POST -H "X-API-Key: <key>" "http://127.0.0.1:8384/rest/db/override?folder=default"
```
`folder` (the folder ID) is mandatory. The call does nothing if the folder is not send only.

## Cautions
- Override deletes remote files that are absent locally, so confirm the local copy is correct first.
- The `order` folder setting has no effect when the folder type is send only.

## Checked
2026-11-04. Read Folder Types, the POST /rest/db/override page and the config page (`order`): purpose, ignore-and-out-of-sync behaviour, Override Changes wording, mandatory `folder`, no-op for other types and the `order` note. Removed the "When to use" bullets and the pairing advice, which the pages do not state.
Method: documentation only; no commands were run.

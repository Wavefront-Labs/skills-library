---
id: computing-software.systems-network-administration.syncthing.rest-restore-file-versions
name: rest-restore-file-versions
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, rest-api, folder-versions, restore-versions]
level: advanced
status: docs-checked
description: "List and restore archived file versions through GET and POST /rest/folder/versions."
sources: ["https://docs.syncthing.net/rest/folder-versions-get.html", "https://docs.syncthing.net/rest/folder-versions-post.html", "https://docs.syncthing.net/users/versioning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restoring versions via REST

## List
`GET /rest/folder/versions?folder=<id>` (added in 0.14.44; `folder` is mandatory) returns the archived files that could be recovered, keyed by relative path, each with a list of versions. Each entry has:
- `versionTime`, when the version was archived
- `modTime`, when the file was last modified before being archived
- `size` in bytes

How many versions are available depends on the File Versioning configuration.

```sh
curl -H "X-API-Key: <key>" "http://127.0.0.1:8384/rest/folder/versions?folder=default"
```

## Restore
`POST /rest/folder/versions?folder=<id>` restores archived versions. It expects an object with attributes named after the relative file paths and timestamps as values matching valid `versionTime` entries from the GET response; `folder` (the folder ID) is mandatory:

```sh
curl -X POST -H "X-API-Key: <key>" "http://127.0.0.1:8384/rest/folder/versions?folder=default" -d '{
  "dir1/dir2/bar": "2022-02-06T20:44:12+01:00",
  "baz": "2022-02-06T20:44:20+01:00"
}'
```
The response is an object containing any error messages that occurred during restoration, with the file path as attribute name.

## Notes
- Versioning applies to changes received from other devices: old versions are archived when a file is deleted or replaced by a change synced from the cluster. If a file is changed locally, Syncthing does not and cannot archive the old version.
- The `versionTime` values must match valid entries from the GET response.

## Checked
2026-11-04. Read the GET and POST /rest/folder/versions pages and File Versioning: parameters, response fields, request body shape, error object, and the remote-changes-only rule. Removed the pagination statement, the restore-one-path-first advice and the "empty object means success" inference, which the pages do not state.
Method: documentation only; no commands were run.

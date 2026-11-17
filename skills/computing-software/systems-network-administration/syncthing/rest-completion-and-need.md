---
id: computing-software.systems-network-administration.syncthing.rest-completion-and-need
name: rest-completion-and-need
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, rest-api, completion, db-need]
level: practitioner
status: docs-checked
description: "Check sync completion and outstanding files with /rest/db/completion, /rest/db/need and /rest/db/status."
sources: ["https://docs.syncthing.net/rest/db-completion-get.html", "https://docs.syncthing.net/rest/db-need-get.html", "https://docs.syncthing.net/rest/db-status-get.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Measuring sync progress

## Completion
`GET /rest/db/completion` returns the completion percentage (0 to 100) and byte / item counts (the example response has `completion`, `globalBytes`, `needBytes`, `globalItems`, `needItems`, `needDeletes`, `remoteState`, `sequence`). Optional parameters:
- `folder`: folder ID; empty or absent means all folders as an aggregate.
- `device`: device ID; empty or absent means the local device.
- With a device and no folder, completion is calculated for all folders shared with that device.

Aggregating folders and defaulting to the local device were added in 1.8.0. `remoteState` was added in 1.20.0: `paused`, `notSharing` or `valid` (remote is sharing back); it is meaningless for aggregated responses and unknown when the remote is not connected.

```sh
curl -H "X-API-Key: <key>" "http://127.0.0.1:8384/rest/db/completion?folder=default&device=<device-id>"
```

## Status
`GET /rest/db/status?folder=<id>` (parameter `folder` is the folder ID) returns `global*`, `inSync*`, `local*`, `need*` and `receiveOnlyChanged*` counters for bytes, files, directories, symlinks and deleted items, plus fields such as `ignorePatterns`, `invalid`, `pullErrors`, `sequence`, `state` and `stateChanged`. `global*` is the cluster latest version, `inSync*` is data locally the same as it, `local*` is data present locally, `need*` is data needed to become up to date.

## Need list
`GET /rest/db/need?folder=<id>` (`folder` mandatory) returns files this device needs to become in sync in three sections: `progress` (currently being downloaded), `queued` (to be downloaded next, in array order) and `rest` (to be downloaded after all queued files). Pagination with `page` and `perpage` is applied across the union of the three sections. With 15 in progress, 3 queued and 12 in rest, `page=2&perpage=10` gives the last 5 progress items, all 3 queued and the first 2 of the rest. The page notes it is an expensive call that increases CPU and RAM usage, to be used sparingly, and that the total count attribute was removed in 0.14.43.

## Checked
2026-11-04. Read the db/completion, db/need and db/status pages: parameters, aggregate and default behaviour, version notes, response fields, pagination example and the expensive-call note. Removed `GET /rest/db/remoteneed` (not on the fetched pages) and the closing "Use" advice.
Method: documentation only; no commands were run.

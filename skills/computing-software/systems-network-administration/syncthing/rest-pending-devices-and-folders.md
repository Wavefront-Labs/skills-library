---
id: computing-software.systems-network-administration.syncthing.rest-pending-devices-and-folders
name: rest-pending-devices-and-folders
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, rest-api, pending, cluster]
level: practitioner
status: docs-checked
description: "List and dismiss pending devices and folder offers through /rest/cluster/pending endpoints."
sources: ["https://docs.syncthing.net/rest/cluster-pending-devices-get.html", "https://docs.syncthing.net/rest/cluster-pending-devices-delete.html", "https://docs.syncthing.net/rest/cluster-pending-folders-get.html", "https://docs.syncthing.net/rest/cluster-pending-folders-delete.html", "https://docs.syncthing.net/events/devicerejected.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pending devices and folders

## Pending devices
`GET /rest/cluster/pending/devices` (added in 1.13.0) lists remote devices that have tried to connect but are not yet configured. Each entry, keyed by device ID, has `time`, `name` and `address`.

`DELETE /rest/cluster/pending/devices?device=<id>` (added in 1.18.0) removes the record; valid values for `device` are those from the GET. It returns status 200 with no content on success, or 500 with a plain text error. A `PendingDevicesChanged` event is generated. For a more permanent effect, also for future connections from the same device ID, ignore the device in the configuration instead.

## Pending folders
`GET /rest/cluster/pending/folders` (added in 1.13.0) lists folders which remote devices have offered but which are not yet shared from our instance to them. The optional `device` parameter returns only folders offered by that device (other offering devices are omitted). Per folder ID, `offeredBy` maps device IDs to:
- `time`
- `label`
- `receiveEncrypted`
- `remoteEncrypted`

`DELETE /rest/cluster/pending/folders?folder=<id>` (added in 1.18.0) removes records about a pending folder. The optional `device` parameter limits it to announcements from that device, or from any device if omitted. It returns 200 with no content, or 500 with a plain text error, and a `PendingFoldersChanged` event is generated. For a more permanent effect, also for future announcements of the same folder ID, ignore the folder in the configuration instead.

## Accepting
Add the device or folder through the configuration (see the rest-config-endpoints skill). The device `autoAcceptFolders` setting automatically adds and syncs folders shared from that remote device under the default path.

## Events
`PendingDevicesChanged` is the replacement for the `DeviceRejected` event, which has been deprecated since 1.13.0 but is still emitted for compatibility.

## Checked
2026-11-04. Read the pending devices GET and DELETE pages, the pending folders GET and DELETE pages, and the DeviceRejected event page: response fields, parameters, status codes, events generated, version notes and the permanent-ignore advice. Narrowed the closing events claim to `DeviceRejected`; the `FolderRejected` page was not read.
Method: documentation only; no commands were run.

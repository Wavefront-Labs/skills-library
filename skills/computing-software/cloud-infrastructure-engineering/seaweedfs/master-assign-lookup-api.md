---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.master-assign-lookup-api
name: master-assign-lookup-api
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [dir-assign, dir-lookup, volume-server-api, master-api]
level: intro
status: docs-checked
description: "Use the raw HTTP APIs: master /dir/assign and /dir/lookup, upload to a volume server, and filer POST/PUT/GET with op=append and ttl."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Master-Server-API
  - https://github.com/seaweedfs/seaweedfs/wiki/Volume-Server-API
  - https://github.com/seaweedfs/seaweedfs/wiki/Filer-Server-API
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# master assign lookup api

Blob flow:
```bash
curl "http://localhost:9333/dir/assign?collection=pics&replication=001&ttl=1d"
# {"count":1,"fid":"3,01637037d6","url":"127.0.0.1:8080","publicUrl":"localhost:8080"}
curl -F file=@photo.jpg http://127.0.0.1:8080/3,01637037d6
curl "http://localhost:9333/dir/lookup?volumeId=3&pretty=y"
curl http://127.0.0.1:8080/3,01637037d6
```
Assign parameters: `count` (extra ids are `<fid>_1`, `_2`), `collection`, `dataCenter`, `rack`, `dataNode`, `replication`, `ttl`, `disk`, `preallocate`, `writableVolumeCount`. Lookup also accepts a full fid. Append `&pretty=y` for readable JSON.

Volume reads accept `width`, `height`, `mode` for images, `Range`, `If-None-Match` and `Authorization` (read JWT). Writes accept `fsync=true`.

Filer API:
```bash
curl -X POST -F file=@a.txt "http://localhost:8888/path/to/a.txt?ttl=1d&mode=0755"
curl -X POST "http://localhost:8888/path/to/a.txt?op=append" --data-binary @more.txt
curl -H "Accept: application/json" http://localhost:8888/path/to/
```
Other parameters: `collection`, `replication`, `maxMB`, `saveInside`, `extract=zip`, `skipCheckParentDir`, `Seaweed-` prefixed headers for extended attributes.

Verify: upload then GET returns identical bytes.

## Checked
Checked 2026-11-09: the assign response shape and parameter list (count, collection, dataCenter, rack, dataNode, replication, ttl, disk, preallocate, writableVolumeCount), lookup by volumeId or full fid, read parameters and headers on volume servers, `fsync`, and the filer POST, append, ttl, mode, listing and extract parameters match the three pages. Removed the unsupported claim that volume writes accept `ttl`. The Filer-Server-API page was searched for each parameter rather than read end to end.
Method: docs-checked 2026-11-09 against the SeaweedFS wiki pages Master-Server-API (first 64 lines), Volume-Server-API (first 60 lines) and Filer-Server-API (parameter table and examples), from a local clone of the wiki.

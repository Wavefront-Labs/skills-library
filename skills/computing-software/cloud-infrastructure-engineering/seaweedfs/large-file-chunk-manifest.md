---
id: computing-software.cloud-infrastructure-engineering.seaweedfs.large-file-chunk-manifest
name: large-file-chunk-manifest
category: computing-software
field: cloud-infrastructure-engineering
product: seaweedfs
tags: [chunk-manifest, cm-true, chunked-upload, large-file]
level: advanced
status: docs-checked
description: "Store very large files as chunk files plus a JSON chunk manifest uploaded with cm=true; append by updating the manifest."
sources:
  - https://github.com/seaweedfs/seaweedfs/wiki/Large-File-Handling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# large file chunk manifest

SeaweedFS reads whole files into memory for concurrency, so big files are split client side. `weed upload` does this for you; third-party clients follow this spec.

Types: chunk files (normal SeaweedFS files) and a chunk manifest, a JSON file:
```json
{"name":"big.bin","mime":"application/octet-stream","size":1048576,
 "chunks":[{"fid":"3,01637037d6","offset":0,"size":524288},{"fid":"4,02a1b2c3d4","offset":524288,"size":524288}]}
```
Create:
1. Split into chunks and upload each normally (they may land on different volumes, enabling parallel reads). Record `fid`, `offset`, `size`.
2. Upload the manifest with MIME type `application/json` and URL parameter `cm=true`. Its file id is the entry point for the large file.

Append or update: upload the new chunks, then re-upload the updated manifest with `cm=true`.

On read, SeaweedFS finds and sends the data chunks listed in the manifest. Chunk sizes need not be equal; the rule of thumb is that a chunk should fit in memory, without creating too many small chunk files.

The filer server and `weed mount` chunk large files automatically and keep the chunk list in filer storage, so none of this is needed there.

Verify: GET the manifest fid and compare size and checksum with the original.

## Checked

Method: docs-checked 2026-11-09 against the SeaweedFS wiki page Large File Handling (raw markdown, read in full). Claims about filer maxMB and op=append were removed as unconfirmed.

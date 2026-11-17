---
id: computing-software.systems-network-administration.rclone.rclone-serve-s3-and-restic
name: rclone-serve-s3-and-restic
category: computing-software
field: systems-network-administration
product: rclone
tags: [serve-s3, serve-restic, auth-key, append-only, private-repos]
level: advanced
status: docs-checked
description: "Serve a remote as an S3 endpoint or as a restic REST backend, including authentication, limits and supported operations."
sources: ["https://rclone.org/commands/rclone_serve_s3/", "https://rclone.org/commands/rclone_serve_restic/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## serve s3

`rclone serve s3 --auth-key ACCESS_KEY_ID,SECRET_ACCESS_KEY remote:path` is an experimental basic S3 server with Signature V4 authentication. Repeat `--auth-key` for several identities; with none, access is anonymous. Via environment the value is CSV encoded and must be quoted: `export RCLONE_AUTH_KEY='"user1,pass1","user2,pass2"'`. Some clients require HTTPS, so configure `--cert` and `--key`.

Behaviour to know:

- Directories in the root are buckets; files in the root are ignored. `CreateBucket` makes root folders but you cannot create empty folders elsewhere. `PutObject` and `DeleteObject` create and clean empty folders unless `--no-cleanup` is set.
- Object keys map to file paths. Keys with `.` or `..` segments, `//`, or a leading or trailing slash are rejected with 400 InvalidArgument.
- `ListObjects` with an empty delimiter uses `/`; any other delimiter triggers a full recursive backend search.
- No versioning; metadata other than mtime is held in memory only.
- Multipart server-side copies do not work (the 5G threshold is the maximum), so files above it fail to copy server-side.
- Supported: ListBuckets, CreateBucket, DeleteBucket, HeadObject, ListObjects, GetObject, PutObject, DeleteObject, DeleteObjects, multipart create/upload/complete/abort, CopyObject. Anything else returns Unimplemented.

## serve restic

`rclone serve restic -v remote:backup` serves restic's REST backend on `localhost:8080` by default (change with `--addr`), letting restic back up to any rclone backend. Point restic at it with `RESTIC_REPOSITORY=rest:http://localhost:8080/` and run `restic init`. Needs restic 0.8.2 or later. `--bwlimit` is respected and `-v` shows access logs. `--cache-objects=false` stops caching listings. `--append-only` disallows deleting repository data and `--private-repos` limits each user to their own repository. `--stdio` runs HTTP2 over stdin/stdout.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.

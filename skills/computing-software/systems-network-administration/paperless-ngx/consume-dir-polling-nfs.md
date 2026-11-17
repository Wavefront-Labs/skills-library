---
id: computing-software.systems-network-administration.paperless-ngx.consume-dir-polling-nfs
name: consume-dir-polling-nfs
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, inotify, nfs, polling, consumer-polling-interval, consumption-directory]
level: practitioner
status: docs-checked
description: "Make the consumer notice new files on NFS or SMB shares by switching from filesystem notifications to polling with PAPERLESS_CONSUMER_POLLING_INTERVAL."
sources:
  - "https://docs.paperless-ngx.com/setup/"
  - "https://docs.paperless-ngx.com/configuration/"
  - "https://docs.paperless-ngx.com/troubleshooting/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumption folder on a network share

## The problem
By default the consumer relies on native filesystem notifications. Network filesystems such as NFS often do not deliver them, so Paperless only sees files that were present at startup and ignores everything added later.

## The fix
Set `PAPERLESS_CONSUMER_POLLING_INTERVAL` to a positive number of seconds:
```bash
PAPERLESS_CONSUMER_POLLING_INTERVAL=10
```
- `0` (the default) means native notifications, which are immediate and cheap.
- Any positive value makes Paperless scan the directory at that interval instead.

## Related settings
- `PAPERLESS_CONSUMER_STABILITY_DELAY` (default 5.0 seconds) is how long a file must stay unchanged before it is consumed. Raise it for slow storage or scanners that write a file in stages.
- With double-sided collation, keep the polling interval lower than the time between the two scans, for example 5 to 10 seconds.
- Heavy consumption with polling can log a harmless duplicate-key error for a tag name; Paperless handles it and still consumes the file.

## Checking
If files still are not consumed, confirm that the folder paperless watches is the one you are using, that the broker and the task processor are running, and look for errors in the output and the failed tasks in the admin interface.

## Checked
2026-11-04. Compared with PAPERLESS_CONSUMER_POLLING_INTERVAL and PAPERLESS_CONSUMER_STABILITY_DELAY in configuration, the consumer entries of troubleshooting (polling, no files added, tag unique constraint) and the double-sided collation section of advanced_usage (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: polling versus native notifications and the default 0, NFS and SMB use, stability delay default 5.0, the 5 to 10 second collation advice, the harmless duplicate-key log line. Replaced the generic "drop a test file" checking advice with the checklist from the troubleshooting page.

Method: documentation only; no commands were run.

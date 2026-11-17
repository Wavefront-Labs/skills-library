---
id: computing-software.collaboration-platform-administration.zulip.s3-cache-and-storage-class
name: s3-cache-and-storage-class
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [s3-cache, s3-storage-class, intelligent-tiering, s3-disk-cache-size]
level: advanced
status: docs-checked
description: "Tune Zulip's nginx S3 cache (memory, disk, inactive time), the nameserver for S3 resolution and S3_UPLOADS_STORAGE_CLASS with Intelligent-Tiering."
sources: ["https://zulip.readthedocs.io/en/latest/production/upload-backends.html", "https://zulip.readthedocs.io/en/latest/production/system-configuration.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# S3 caching and storage class

Zulip keeps a local nginx cache of recently served uploads even though durable storage is S3. Tune it in the `[application_server]` section of `/etc/zulip/zulip.conf`:

- `s3_memory_cache_size`: in-memory size of the cache index, default 1MB, about 8 thousand entries.
- `s3_disk_cache_size`: on-disk size of the cache contents, default 200MB.
- `s3_cache_inactive_time`: longest time since last use, default 30 days. Contents are immutable, so this is only a secondary size limit.

Defaults suit small to medium deployments. Large or image-heavy ones should raise disk cache to several gigabytes and the memory index accordingly, and also if the storage is far from the server, since misses cost more.

nginx needs an explicit DNS nameserver to resolve S3 hostnames. Zulip uses the first one in `/etc/resolv.conf`; override with `nameserver` in `zulip.conf`, then run `~zulip/deployments/current/scripts/zulip-puppet-apply`.

Storage class: set `S3_UPLOADS_STORAGE_CLASS` in `settings.py` to one of `STANDARD`, `STANDARD_IA`, `ONEZONE_IA`, `REDUCED_REDUNDANCY`, `GLACIER_IR` or `INTELLIGENT_TIERING`. Intelligent-Tiering can save money for large deployments, since uploads are accessed often at first then age out.

The setting does not change existing objects. Convert them with an in-place copy:

```
aws s3 cp --storage-class INTELLIGENT_TIERING --recursive s3://your-bucket-name/ s3://your-bucket-name/
```

That incurs a one-time lifecycle transition cost.

## Checked

2026-11-08. Checked: read against the Zulip upload-backends page (docs/production/upload-backends.md, read in full) and the system-configuration page (read in full). Removed: nothing.

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.varnish-cache.storage-backends
name: storage-backends
category: computing-software
field: systems-network-administration
product: varnish-cache
tags: [stevedore, malloc, file-storage, varnishd-s]
level: practitioner
status: docs-checked
description: "Choose and size Varnish storage backends with -s: default, malloc, umem, file and persistent, with size suffixes, memory overhead, file options and multiple stores."
sources:
  - https://www.varnish.org/docs/users-guide/storage-backends/
  - https://www.varnish.org/docs/reference/varnishd/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# storage backends

`-s [name=]type[,options]`, repeatable; the name appears in logs, VCL (`storage.<name>`) and statistics; unnamed stores are s0, s1 and so on. With no `-s` the default is `-s default,100m`. Storage backends are also called stevedores. Built-in backends cache full objects only.

- `default[,size]`: alias for umem where available, otherwise malloc.
- `malloc[,size]`: virtual-memory backend using whatever malloc() is in effect; the OS may page it to swap. Size is bytes, or K/M/G/T (kibi-, mebi-, gibi-, tebibytes, either case). Default size is unlimited. Size is net memory (metadata, body segments, engine metadata). Real use is higher: about 1KB per object outside the store, and fragmentation typically makes the malloc implementation use two to four times more; Transparent Hugepage on Linux can amplify this. Speed is memory-bound; if the data set exceeds memory, performance depends on OS paging.
- `umem[,size]`: better alternative where libumem is available (OpenSolaris-descended systems); otherwise like malloc. If libumem is already loaded at startup, varnishd prints a notice and recommends `UMEM_OPTIONS=perthread_cache=0,backend=mmap`, which must be set before starting.
- `file,path[,size[,granularity[,advice]]]`: mmap of a file, with no cache persistence. `path` may be the backing file or a directory (a temporary file is created and unlinked). With an existing file and no size, its size is used; for a non-existent file, size is required. Existing files are truncated or expanded to size without pre-allocation, causing fragmentation on rotating disks; pre-creating the file with dd reduces it. `granularity` rounds allocations (default the larger of page size or filesystem block size per the reference; reduce it for many small objects). `advice` is `normal`, `random` (default) or `sequential`; the guide says large objects on rotational disks on Linux should benefit from sequential. Needs enough virtual memory for the file (ulimit -v, cgroups).
- `deprecated_persistent,path,size` (experimental): stores objects in silos like a circular buffer so most objects survive shutdown; bans added while a silo is offline are not applied to it, so banned objects can reappear. The reference says it has multiple issues and will likely be removed. (The reference spells the type `persistent`.)

Sizing hint: n concurrent hits on 1GB objects need at least n GB; for uncacheable objects n x transit_buffer. Watch `n_lru_nuked` in varnishstat; sustained evictions mean the cache is too small. The CLI command `storage.list` lists storage devices.

## Checked

Method: 2026-11-08 docs-only read of the storage-backends guide; the -s section of the varnishd reference was checked by search. Added overhead, umem, file and persistent details. Removed the earlier "Verify" line as an invented step (storage.list is a real CLI command, but neither page presents it as a check).

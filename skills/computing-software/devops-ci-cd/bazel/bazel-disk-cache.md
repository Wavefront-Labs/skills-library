---
id: computing-software.devops-ci-cd.bazel.bazel-disk-cache
name: bazel-disk-cache
category: computing-software
field: devops-ci-cd
product: bazel
tags: [disk-cache, disk-cache-flag, nodisk-cache, disk-cache-gc, cache-garbage-collection]
level: practitioner
status: docs-checked
description: "Enable the Bazel disk cache to share outputs between checkouts and branches, and bound its size with garbage collection."
sources: ["https://bazel.build/remote/caching"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bazel disk cache

A directory on disk can act as a remote cache, useful when switching branches or keeping several checkouts of the same project.

```
build --disk_cache=/path/to/build/cache
build --disk_cache=~/.cache/bazel-disk     # ~ expands to the current user's home
build --disk_cache                          # no value: <outputUserRoot>/cache/disk
build --nodisk_cache                        # disable explicitly
```

The `~` alias makes the flag safe to put in a checked-in `.bazelrc` for all developers. With no value, the cache goes under the output user root next to the repository cache.

Garbage collection (Bazel 7.4 and later): set `--experimental_disk_cache_gc_max_size` and/or `--experimental_disk_cache_gc_max_age`. Bazel collects while idle between builds; the idle timer is `--experimental_disk_cache_gc_idle_delay`, default 5 minutes. The docs also point to a tool that runs garbage collection on demand.

Pitfall: modifying source files during a build can upload invalid results to any cache. `--experimental_guard_against_concurrent_changes` enables detection.

## Checked

2026-11-04. Read against the Bazel docs page(s): Remote Caching (disk cache section) (bazel.build). Commands, flags, defaults, values and behaviour described above match them. Removed: the closing Verify line.
Method: documentation only; no commands were run.

---
id: computing-software.devops-ci-cd.rundeck.tune-file-descriptors-and-heap
name: tune-file-descriptors-and-heap
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, file-descriptors, jvm-heap, xmx, oom-killer]
level: advanced
status: docs-checked
description: "Fix 'Too many open files' and heap exhaustion on a Rundeck server: raise nofile limits, set Xmx and Xms per install type, and tell Java OOM from the Linux OOM killer."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/administration/maintenance/tuning-rundeck.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
File descriptors. Symptom in `service.log`: `Too many open files`. Check and count:

```bash
ulimit -n
lsof -p <rundeck pid> | wc -l
```

If low (for example 1024), raise it in `/etc/security/limits.conf`:

```
rundeck hard nofile 65535
rundeck soft nofile 65535
```

The system-wide limit is `/proc/sys/fs/file-max`. The ulimit can also be set in the `rundeckd` startup script or the profile. Restart Rundeck.

Heap. Symptom: `java.lang.OutOfMemoryError: Java heap space`. Defaults set by the installer are 1024 MB max and 256 MB initial. Inspect with `egrep '(Xmx|Xms)' /etc/rundeck/profile` (launcher: `$RDECK_BASE/etc/profile`).

Override in `/etc/sysconfig/rundeckd` (RPM) or `/etc/default/rundeckd` (DEB); launcher installs edit `$RDECK_BASE/etc/profile`:

```bash
RDECK_JVM_SETTINGS="$RDECK_JVM_SETTINGS -Xmx4096m -Xms1024m"
```

Sizing drivers: user sessions, concurrent threads, concurrent jobs, managed node count.

Gotcha: process memory exceeds `-Xmx` (metaspace, thread stacks, direct buffers, GC), and local jobs run as separate OS processes. If the host runs out of memory the Linux OOM killer can end Rundeck with no Java stack trace. Confirm with:

```bash
dmesg -T | grep -i -E 'out of memory|killed process'
```

Rundeck 6.0 raises baseline memory (Grails 7, Spring Boot 3), so revisit heap after upgrading from 5.x.

## Checked

2026-11-04: the file descriptor symptom, checks and limits, heap symptom, defaults, profile and override files, the JVM settings line, the sizing drivers and the OOM killer guidance confirmed against the Rundeck Tuning page.

Method: documentation only; no commands were run.

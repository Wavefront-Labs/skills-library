---
id: computing-software.systems-network-administration.openldap.slapd-tuning
name: slapd-tuning
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, tuning, performance, threads, olcthreads, indexing, logging]
level: advanced
status: docs-checked
description: "Tune OpenLDAP slapd: index choices, thread counts, logging cost, index_param warnings, filesystem and memory advice, with documented defaults."
sources:
  - https://www.openldap.org/doc/admin26/tuning.html
  - https://www.openldap.org/software/man.cgi?query=slapd-config&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/software/man.cgi?query=slapd-mdb&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slapd tuning
Indexing:
- `objectClass eq` first, then attributes in filters (`cn`, `sn`, `givenname`, `mail`) with only the types needed.
- Skip presence indexes in most cases; substring and approximate indexes are large; unused indexes still cost CPU, disk and memory.
- Back-mdb keys cover 2^16 entries by default; beyond that precision degrades over time.
- Log line `index_param failed (18)` means an equality filter hit an unindexed attribute.

Threads: `olcThreads` (maximum primary thread pool, default 16, minimum 2) and `olcToolThreads` (tool mode, default 1). Guide advice: about 4 threads per physical core; more threads slow reads but may help write-heavy loads; 16 is the apparent upper bound for read performance.

Logging: keep the default `loglevel stats` (256). Do not set 0 in production. For debug, capture stderr via `-d` instead of syslog, which can drop messages. On Linux, asynchronous syslog writes reduce overhead.

MDB: size `maxsize` generously; `searchstack` defaults to 16 and deeper filters cost memory; `rtxnsize` 10000.

Hardware: scale memory, test filesystems for your workload (the authors saw EXT2 and JFS beat EXT4 and BTRFS on writes), and give each database its own disks.

Verify: watch `cn=Monitor` thread and waiter counters under load; see the monitor-backend skill.

## Checked

2026-11-04. Confirmed against the Administrator's Guide Tuning chapter and slapd-config(5): objectClass eq first and the example filter attributes, presence and substring index costs, back-mdb 2^16 entries per key, index_param failed (18) message meaning, olcThreads default 16 minimum 2, olcToolThreads default 1, 4 threads per real core and 16 as upper bound for reads, loglevel stats (256) default, loglevel 0 not ideal, debug flag with stderr instead of lossy syslog, asynchronous syslog on Linux, EXT2 and JFS write observation, separate disks per database, plus slapd-mdb(5) searchstack and rtxnsize defaults and the Monitor Threads and Waiters entries.

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.openldap.mdb-envflags-and-sync
name: mdb-envflags-and-sync
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, envflags, dbnosync, writemap, mapasync, nordahead, checkpoint, mdb]
level: advanced
status: docs-checked
description: "Trade durability for speed on OpenLDAP MDB with dbnosync and envflags (nosync, nometasync, writemap, mapasync, nordahead), and use checkpoint with nosync."
sources:
  - https://www.openldap.org/software/man.cgi?query=slapd-mdb&sektion=5&apropos=0&manpath=OpenLDAP+2.6-Release
  - https://www.openldap.org/doc/admin26/slapdconfig.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MDB envflags and sync
Defaults: full sync on every commit, no envflags set.

- `dbnosync` (`olcDbNosync: TRUE`): skip immediate sync; faster, but an OS crash can lose transactions.
- `envflags {nosync,nometasync,writemap,mapasync,nordahead}` (`olcDbEnvFlags`):
  - `nosync`: same as dbnosync.
  - `nometasync`: flush data on commit but skip the meta page sync; the last transaction can be lost on an OS crash. `nosync` takes precedence if both are set.
  - `writemap`: writable memory map for faster writes; stray writes from bugs can corrupt the database.
  - `mapasync`: asynchronous flushes; only meaningful with `writemap`, no effect with `nosync`.
  - `nordahead`: disable readahead; helps random access when the database is larger than RAM; not implemented on Windows.
- `checkpoint <kbyte> <min>`: only needed with `dbnosync`; a non-zero minute value starts an internal task that flushes. The kbyte part is not implemented. Example `checkpoint 1024 10`.

Example:
```
dbnosync TRUE
checkpoint 1024 10
```

## Checked

2026-11-04. Confirmed against slapd-mdb(5) and the Administrator's Guide slapd.d chapter: full sync on every commit by default, dbnosync and olcDbNosync, the five envflags with their descriptions (nosync same as dbnosync, nometasync precedence, writemap corruption risk, mapasync needing writemap and ignored with nosync, nordahead not on Windows), checkpoint only needed with dbnosync, kbyte unimplemented, non-zero min starting an internal task, olcDbCheckpoint 1024 10, olcDbEnvFlags. Removed the mdb_copy sparse note and the backup advice, which those pages do not state.

Method: documentation only; no commands were run.

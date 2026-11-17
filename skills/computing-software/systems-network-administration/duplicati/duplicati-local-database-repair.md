---
id: computing-software.systems-network-administration.duplicati.duplicati-local-database-repair
name: duplicati-local-database-repair
category: computing-software
field: systems-network-administration
product: duplicati
tags: [local-database, repair-command, database-recreate, remote-verification, server-database, list-broken-files]
level: practitioner
status: draft
description: "Know what Duplicati's per-backup local database holds, how to rebuild it from the remote data and what is lost when you do."
sources: ["https://docs.duplicati.com/detailed-descriptions/database-and-storage/the-local-database", "https://docs.duplicati.com/technical-details/database-versions"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# The Duplicati local database

Duplicati uses two kinds of databases: one for the Server and one for each backup, stored alongside the Server database. With only the backup files and the passphrase you can restore; the same, plus the configuration, is enough to continue the backup on another machine. The local database mainly makes operations faster.

It is a compact view of what is stored remotely and can always be recreated from the remote data. Only log messages and the hashes of the remote volumes are lost on recreation; the logs are mostly informational.

Before a backup, Duplicati does a quick scan of the destination to verify that it looks as expected. This check matters because backing up on the assumption that data exists could produce a backup that can only be partly restored. If the check fails, the backup stops with an error rather than proceeding.

For some errors the `repair` command fixes the problem, provided the data it needs is still present; if there is no real way to recover, there may be other options in the recovery documentation. In rare cases the database itself is corrupt; then it is safe to delete the local database and run repair. Recreating can take a while, but no data is lost, and restores work without a database (a temporary one is built).

`list-broken-files` compares what should be in the backup with what is at the remote location, and purge commands can remove broken files from the backup set.

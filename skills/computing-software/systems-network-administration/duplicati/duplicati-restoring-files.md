---
id: computing-software.systems-network-administration.duplicati.duplicati-restoring-files
name: duplicati-restoring-files
category: computing-software
field: systems-network-administration
product: duplicati
tags: [restore-files, direct-restore, restore-from-configuration, restore-passphrase, partial-database]
level: practitioner
status: draft
description: "Restore from Duplicati using an existing configuration, an exported configuration file or direct restore from the backup files with only the destination and passphrase."
sources: ["https://docs.duplicati.com/getting-started/restoring-files"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Restoring files with Duplicati

Start on the Restore page. If the backup configuration exists on the machine, pick it and click Restore; this is the fastest path because Duplicati can query its local database. Without a local database it must fetch enough from the remote storage to build a partial database first.

Restore from configuration: if you exported the backup configuration, use Start under "Restore from configuration" and provide the file. If that file is encrypted you will be asked for its passphrase, which is not necessarily the one that encrypts the backup. If you will restore repeatedly, import the configuration and rebuild the database instead.

Direct restore from backup files: Duplicati only needs to know how to reach the files and the encryption passphrase. Without the passphrase, restore is impossible. This suits restoring on a different machine than the one that made the backup, but downloads and processes more data, so it is not recommended for regular use. Enter the same destination details used originally (cloud details are usually available from the provider account), use Test now, leave the passphrase empty if unencrypted, then Continue; Duplicati examines the destination and lists the backups present.

Then choose the files to restore: Duplicati selects the most recent version first and lets you pick another.

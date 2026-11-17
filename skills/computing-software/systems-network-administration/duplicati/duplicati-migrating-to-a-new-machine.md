---
id: computing-software.systems-network-administration.duplicati.duplicati-migrating-to-a-new-machine
name: duplicati-migrating-to-a-new-machine
category: computing-software
field: systems-network-administration
product: duplicati
tags: [migrate-machine, copy-server-database, disable-db-encryption, import-export-configuration, repair-after-migration]
level: practitioner
status: draft
description: "Move Duplicati to a new computer by copying its data folder, importing exported job configurations or recreating the backup by hand, then repairing the database."
sources: ["https://docs.duplicati.com/detailed-descriptions/configuration-and-management/migrating-duplicati-to-a-new-machine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Migrating Duplicati to a new machine

Restoring files onto a new machine follows the normal restore flow. To continue the backups there, pick the path that matches what you still have. Restores work across operating systems, but a Windows backup cannot be continued from Linux or macOS and vice versa because paths differ. Never run backups to one destination from two machines; stop the old machine's automatic backups before migrating, or one instance will see unexpected remote changes.

Old machine available: copy the Duplicati data folder holding `Duplicati-server.sqlite` and the other databases. This is fastest because everything is kept. From 2.3 the configuration database is encrypted by default, so decrypt it first: stop Duplicati, start it once with `--disable-db-encryption=true`, then stop it again. Move the folder to the same location on the new machine and start Duplicati; the new machine encrypts the database with its own key. After a long gap the first run may trigger extra checks.

Configurations available: import the exported job files in the UI; you may modify details before saving. Then run repair so Duplicati recreates the local database from the remote data; after that backups run as before.

Nothing available: re-create the backup by hand with at least the destination details, the passphrase and the sources, run repair, then back up as normal.

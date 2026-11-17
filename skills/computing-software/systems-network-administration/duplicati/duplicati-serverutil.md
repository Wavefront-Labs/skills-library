---
id: computing-software.systems-network-administration.duplicati.duplicati-serverutil
name: duplicati-serverutil
category: computing-software
field: systems-network-administration
product: duplicati
tags: [serverutil, server-util-login, list-backups, run-backup-from-cli, export-backup-config, refresh-token]
level: practitioner
status: docs-checked
description: "Script a running Duplicati Server with ServerUtil to log in, list backups, queue runs and export configurations without opening the web UI."
sources: ["https://docs.duplicati.com/duplicati-programs/command-line-interface-cli-1/serverutil"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Scripting the Duplicati Server with ServerUtil

ServerUtil talks to a running Duplicati Server through its API, the same requests the web UI makes, and replaces the unmaintained duplicati_client script. The binary is `Duplicati.CommandLine.ServerUtil.exe` on Windows and `duplicati-server-util` on Linux and macOS.

Login: by default it reads the Server database from the current user's default path to find the URL and credentials, so for a service run it as Administrator or root. Point to another database with `duplicati-server-util login --server-datafolder=<database folder path>`. If the database is encrypted, write protected or otherwise unreadable, pass the URL and password. For scripts, `duplicati-server-util login --password=<password> --hosturl=<hosturl>` stores a refresh token in the settings file so later calls need only the host URL; add `--settings-encryption-key=<key>` to protect the stored token. Revoke it with `logout --hosturl=<hosturl>`.

Backups: `list-backups` shows every configuration with name and ID. Commands accept the ID or the case-insensitive name; the ID is preferred as it stays stable. `run <backup id or name>` queues the backup, which starts when the queue is empty. `export <backup id or name> --encryption-passphrase=<passphrase>` writes the configuration to a local file, encrypted with that passphrase.

## Checked

2026-11-04. Confirmed against the ServerUtil page. Nothing removed.

Method: documentation only; no commands were run.

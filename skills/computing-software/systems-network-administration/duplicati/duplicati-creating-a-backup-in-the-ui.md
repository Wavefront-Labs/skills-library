---
id: computing-software.systems-network-administration.duplicati.duplicati-creating-a-backup-in-the-ui
name: duplicati-creating-a-backup-in-the-ui
category: computing-software
field: systems-network-administration
product: duplicati
tags: [backup-wizard, passphrase, source-selection, destination-test, backup-schedule, backup-job]
level: intro
status: draft
description: "Walk through Duplicati's five-step backup setup in the web UI, with the passphrase, destination folder and scheduling rules that avoid common mistakes."
sources: ["https://docs.duplicati.com/getting-started/set-up-a-backup-in-the-ui", "https://docs.duplicati.com/getting-started/running-a-backup"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Creating and running a backup in the UI

Open the UI (use the TrayIcon's Open entry if needed), click Add backup, then Add a new backup. From Duplicati 2.4.0.1 the five steps are: basic configuration, source data, storage destination, schedule, then retention and miscellaneous. In earlier versions the destination step comes before the source step.

1. Basic configuration: a name and optional description (display only), an encryption method and a passphrase. Store the passphrase safely; nothing can be recovered if it is lost. A passphrase generator and strength meter are built in. Encryption adds minor overhead; opt out only if you control the storage.
2. Source data: pick files and folders. A selected folder includes its subfolders; unticking an item excludes it. Filters can add include and exclude rules.
3. Storage destination: each backup needs its own folder; two backups sharing a destination folder will keep breaking each other. Use Test now to check the connection.
4. Schedule: the built-in scheduler keeps backups current; if you disable it, trigger runs with ServerUtil.
5. Retention and miscellaneous: remote volume size (the default suits cloud storage and limited links; raise it for fast or local networks) and retention. Smart backup retention fits most users.

Run any time with the Start button. The first run is the slowest since it processes every file; later runs process only changes. A progress bar shows at the top. ServerUtil can start a backup from the command line without the UI.

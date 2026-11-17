---
id: computing-software.networking-hardware-and-wireless.opnsense.alias-import-export
name: alias-import-export
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [aliases, alias-import, alias-export, json]
level: intro
status: docs-checked
description: "Bulk-edit OPNsense aliases through the JSON download and upload buttons, with validation before merge."
sources: ["https://docs.opnsense.org/manual/aliases.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alias import and export

The Firewall > Aliases page has download and upload buttons in the footer of the table. Download produces a JSON file listing every alias on the system; upload merges aliases from a JSON file into the running configuration.

Imported data goes through the same validation as entries typed into the dialog. If anything is invalid the import fails and shows a list of errors, so a broken alias cannot slip into the configuration. That makes the pair useful for migrations or for sweeping edits: download, change many entries in a text editor (rename, retarget, bulk add), then upload.

A practical routine: export before a large rework to keep a restore point, edit the JSON, upload, then check the result in the overview and under Firewall > Diagnostics > Aliases before applying changes on rules that depend on the alias. After import, remember that rules using changed aliases with state tracking may need their states cleared to pick up the new contents.

For programmatic edits of single entries, the alias_util API endpoints add or remove addresses without touching the rest of the alias; see the Add new entries using our API section of the Aliases manual page.

## Checked

2026-11-03. Read the Aliases manual page (aliases.html) on docs.opnsense.org and confirmed the claims above against them. Removed: a vague pointer to an 'external alias skill'.
Method: documentation only; no commands were run.

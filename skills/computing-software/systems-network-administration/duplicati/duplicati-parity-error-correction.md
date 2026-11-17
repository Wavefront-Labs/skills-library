---
id: computing-software.systems-network-administration.duplicati.duplicati-parity-error-correction
name: duplicati-parity-error-correction
category: computing-software
field: systems-network-administration
product: duplicati
tags: [parity-module, par2, parity-redundancy-level, bit-rot, par2-program-path]
level: practitioner
status: docs-checked
description: "Add PAR2 error-correction files next to Duplicati volumes so damaged remote files can be repaired when downloaded for restore or compact."
sources: ["https://docs.duplicati.com/detailed-descriptions/database-and-storage/parity-error-correction"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Parity error correction in Duplicati

Available from Duplicati 2.4.0.0. Remote files can be damaged by disk bit rot or a storage service error. Duplicati detects a damaged volume but cannot repair it alone; with a parity module it stores error-correction data next to each volume. Parity is off by default; the only module is `par2` (PAR2 format), which needs the `par2` (par2cmdline) program installed.

Enable with `--parity-module=par2` in the backup's advanced options. When a dblock volume or dlist file is uploaded, a companion file with the same name plus `.par2` is uploaded too. Index (dindex) files get none. The companion is deleted together with its volume.

When a downloaded volume fails the integrity check, for example in a restore or compact, Duplicati tries to repair the downloaded copy with the companion file. The verification after a backup and the `test` command do not repair, so they still report the damage.

Options: `--parity-redundancy-level` (default 5, percent of volume size; higher repairs more damage but costs storage and upload time), `--par2-program-path` when par2 is not on the path, and `--par2-extra-options` for extra par2 create arguments. Only volumes uploaded after enabling get parity data.

## Checked

2026-11-04. Confirmed against the Parity error correction page. Nothing removed.

Method: documentation only; no commands were run.

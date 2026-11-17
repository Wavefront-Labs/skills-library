---
id: computing-software.systems-network-administration.linux.journald-forward-secure-sealing
name: journald-forward-secure-sealing
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, journald, forward-secure-sealing, journal-verify, journalctl-setup-keys, log-integrity, tamper-evidence]
level: advanced
status: docs-checked
description: "Make journal tampering detectable with Forward Secure Sealing: journalctl --setup-keys, Seal=yes, storing the verification key offline and running journalctl --verify."
sources:
  - https://github.com/systemd/systemd/blob/main/man/journalctl.xml
  - https://github.com/systemd/systemd/blob/main/man/journald.conf.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Journal Forward Secure Sealing (FSS)

**Goal:** if an attacker gets root later and edits old journal entries, verification exposes it.
FSS seals the journal at intervals with an evolving key; old sealing keys are discarded.

## Setup
```bash
mkdir -p /var/log/journal            # persistent storage required (Storage=persistent, or auto with this directory present)
journalctl --setup-keys --interval=15min    # 15min is the default interval
```
This generates a sealing key and a **verification key**. The sealing key is stored in the journal data
directory and must stay on the host; store the verification key OFF the machine (password manager, vault).
`Seal=` in `journald.conf` defaults to yes; FSS applies to persistent journal files once a sealing key exists
(`journalctl --setup-keys --force` recreates keys). Restart `systemd-journald` after changing its config.

## Verify
```bash
journalctl --verify --verify-key=<verification-key>    # internal consistency plus authenticity of sealed files
journalctl --verify                  # without key: checks internal consistency only
```
Schedule a verification from a separate trusted host (or after copying journals) — verifying on a
compromised host with its own tools is weak.

## Limits
- Shorter intervals increase CPU use but shorten the time range of undetectable alteration (journalctl man page).
- Without the verification key only internal consistency can be checked, so keep it safe.
- FSS gives tamper evidence for journal files; it is not a substitute for forwarding logs to another host.

## Verify
- [ ] `journalctl --verify --verify-key=...` reports no failure for any journal file.

## Checked

Checked 2026-10-26 against systemd/systemd main (last commit 2026-10-25) man/journalctl.xml and man/journald.conf.xml. Confirmed: --setup-keys, --interval default 15min and its trade-off, --verify and --verify-key semantics, --force recreating keys, Seal= default yes, sealing key staying on the host while the verification key is stored externally, Storage= persistent/auto behaviour. Removed: the QR code claim, the exact fss file path, PASS/FAIL output format, and the unsourced limits (whole-file deletion, no recovery); the unverifiable LWN link was replaced by the man pages.

Method: documentation only; no commands were run.

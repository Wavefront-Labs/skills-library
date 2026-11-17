---
id: computing-software.systems-network-administration.backup-and-recovery.backup-scope-and-exclusions
name: backup-scope-and-exclusions
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-scope, backup-exclusions, backup-strategy, protection-coverage]
level: practitioner
status: docs-checked
description: "Decide what to back up and what to exclude: scope from the inventory, documented exclusions, and restic exclude options and their limits."
sources:
  - https://restic.readthedocs.io/en/stable/040_backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup scope and exclusions

## Scope
Build scope from the business impact analysis and an inventory, not from "what we already back up". Include business data, the systems needed to recover (identity, DNS, certificate authority, backup server configuration, network and hypervisor configs, secrets vaults, infrastructure code) and the keys that protect the backups themselves. Include recovery documentation, kept offline too.

## Often forgotten
Cloud resources created outside infrastructure code, SaaS admin settings, licence files, break-glass MFA material, workstation-only data, container persistent volumes.

## Exclusions
Exclude only what can be recreated or is noise (caches, temp files, swap), and document every exclusion with a reason and an owner. Review the list on a schedule.

### restic exclude options
- `--exclude`, and `--iexclude` which ignores the case of paths; `--exclude-file` and `--iexclude-file` read patterns from a file (environment variables in exclude files are expanded, a literal dollar sign is written `$$`, and `~` is not expanded).
- `--exclude-caches` excludes a folder's content if it contains the special CACHEDIR.TAG file.
- `--exclude-if-present foo` excludes a folder's content if it contains a file called foo.
- `--exclude-larger-than size` excludes files larger than the size.
- `--exclude-cloud-files` excludes online-only cloud files (OneDrive Files On-Demand, iCloud Drive); only supported on Windows and macOS.
- `--one-file-system` stops restic crossing filesystem boundaries; virtual filesystems such as /proc count as different and are excluded. It is currently unsupported on Windows and makes the backup fail immediately.
- A pattern starting with an exclamation mark cancels an earlier match, like gitignore; once a directory is excluded, files inside it cannot be re-included.
- Excludes do not apply to sources passed explicitly: `restic backup ~/work.txt` always backs up that file. Content inside an explicitly passed directory is still filtered.

## Prove coverage
Reconcile the inventory (VMs, databases, SaaS tenants, shares) against backup job membership regularly and report unprotected items. Restore-test a sample from every data class, not only VMs.

## Gotchas
- Wildcard exclusions grow silently: a `*.tmp` pattern can match an application's real data.
- "It's in the cloud" is not a backup.

## Verify
Coverage report shows every in-scope item protected or formally excepted; the exclusion list was reviewed with data owners recently.

## Checked

2026-11-09. Confirmed against the restic "Backing up" page (the exclude options above, explicit-source rule, `--one-file-system` and its Windows limitation). Removed: the NIST SP 800-34 source (landing page, not read), the table of Windows and Linux file names and cache paths, `node_modules`, Git LFS, TOTP seed and database-dump specifics, and the weekly and 12-month intervals (not on the page). Scope lists are practice advice, not product facts.

Method: documentation only; no commands were run.

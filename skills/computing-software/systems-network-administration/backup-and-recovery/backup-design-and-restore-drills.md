---
id: computing-software.systems-network-administration.backup-and-recovery.backup-design-and-restore-drills
name: backup-design-and-restore-drills
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup, backup-and-recovery, disaster-recovery, dr, 3-2-1, 3-2-1-1-0, rpo, rto, immutable-backup, object-lock, air-gap, offline-backup, ransomware, retention, gfs, grandfather-father-son, restore-test, restore-drill, dr-runbook, restic, borg, borgbackup, veeam, proxmox-backup-server, snapshots, encryption, deduplication]
level: practitioner
status: gated
description: "Design backups that survive ransomware: 3-2-1-1-0, RPO/RTO, immutable and offline copies, GFS retention, restic/borg examples, and scheduled restore drills."
sources:
  - https://restic.readthedocs.io/
  - https://borgbackup.readthedocs.io/
  - https://www.cisa.gov/stopransomware
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup design and restore drills — a backup you have not restored is a hope

**Goal:** backups sized to business needs, out of an attacker's reach, kept for the
right time, and proven by regular restores and a written DR runbook.

## 1. Start from RPO and RTO, per system
- **RPO** (Recovery Point Objective): how much data loss is acceptable → backup frequency.
- **RTO** (Recovery Time Objective): how long until it works again → restore method.

Illustrative tiers (set your own with the business owner):

| Tier | Example | RPO | RTO | Method |
|---|---|---|---|---|
| 1 | Order DB, identity | 15 min | 1–4 h | DB log shipping / replication **plus** backups |
| 2 | File server, app servers | 24 h | 24 h | Nightly image/file backup |
| 3 | Archives, test | 7 days | days | Weekly |

Agree these with the business owner, in writing. Test that the backup system can
actually hit the RTO: restoring 10 TB over 1 Gb/s takes about 22 hours at full line rate, before any overhead.
Replication is not backup: it faithfully replicates deletions and encryption.

## 2. 3-2-1-1-0 (gated: unconfirmed, source is paywalled or blocked)
- **3** copies of data (production + 2 backups)
- **2** different media/storage systems
- **1** off-site
- **1** offline, air-gapped or **immutable**
- **0** errors on verified restores

## 3. Survive ransomware
Attackers look for and delete backups first, using the same admin credentials.
- **Immutable copies:** S3 Object Lock in *compliance* mode (a protected version cannot be
  overwritten or deleted by any user, including the account root; governance mode can be
  overridden by principals with `s3:BypassGovernanceRetention`), hardened Linux repositories with
  immutability, or tape/removable disks rotated off-site.
- **Separate identity:** backup server not domain-joined (or in a separate management
  domain), unique admin accounts with MFA, no backup credentials stored on production hosts.
  Restrict delete rights: the client should be able to append, not prune
  (`borg serve --append-only`, restic `rest-server --append-only`).
- **Encrypt** backups; store the keys/passphrases **outside** the backed-up environment
  (sealed in a password manager plus an offline copy). Lost key = lost backups.
- Keep enough history to predate a quiet intrusion.

## 4. Retention: GFS
Grandfather-Father-Son: e.g. 14 daily, 8 weekly, 12 monthly (yearly copies only
where law or contract requires). Legal retention may require keeping data; privacy law
may require *not* keeping it longer than needed. Document both.

## 5. Tool examples
**restic** (dedup, encryption, S3/B2/SFTP/rest-server backends):
```bash
export RESTIC_REPOSITORY=s3:https://<S3_ENDPOINT>/<BUCKET>/<HOST>
export RESTIC_PASSWORD_FILE=/etc/restic/passphrase      # chmod 600
restic init
restic backup /etc /srv --exclude-caches --tag nightly
restic forget --keep-daily 14 --keep-weekly 8 --keep-monthly 12 --prune
restic check --read-data-subset=5%
restic restore latest --target /tmp/restore --include /srv/app
```
**BorgBackup** (dedup, encryption, SSH backends):
```bash
borg init --encryption=repokey-blake2 ssh://backup@<BACKUP_HOST>/./<HOST>
borg create --stats --compression zstd ::'{hostname}-{now}' /etc /srv
borg prune --keep-daily 14 --keep-weekly 8 --keep-monthly 12
borg compact
borg check
```
With `repokey` modes, the key is inside the repo but useless without the passphrase;
export it too (`borg key export`). Run `prune`/`forget` from a separate trusted host
when clients are append-only (borg's `--append-only` only affects the repository's low-level
structure, so check what a prune does in your version). Databases: back up a consistent
dump or use the DB's native backup, never just copy live data files. Schedule via systemd timers and alert on **missing** success, not just on
errors.

## 6. Restore drills
- **Monthly:** restore random files and one full VM/server into an isolated network;
  check the app starts and data is current to within RPO. Time it against the RTO.
- **Quarterly:** restore a tier-1 system end to end, including the order of
  dependencies (identity/AD and DNS first, then databases, then apps).
- **Yearly:** full DR exercise or tabletop with the people who would actually do it.
- Automate integrity checks (`restic check`, `borg check`, vendor restore-verification
  features) but they do not replace a human-run restore.
Record date, what was restored, time taken, issues found, and fixes.

## 7. DR runbook (keep a printed/offline copy)
1. Declaration criteria and who can declare a disaster; contact tree.
2. Recovery order and dependencies; RTO per system.
3. Where backups live, how to get credentials and keys when AD/SSO is down.
4. Step-by-step restore per system, with commands, written so a competent colleague
   (not the author) can follow it.
5. Validation checks and handback to the business; post-incident review.

## Verify
- [ ] Every system has an agreed RPO/RTO, and its backup schedule meets the RPO.
- [ ] At least one copy is immutable or offline and the production admin account cannot delete it.
- [ ] Encryption keys are stored outside the environment being backed up, and retrievable.
- [ ] A restore was performed this month and its time fits the RTO.
- [ ] Alerts fire when a backup job does not report success.
- [ ] DR runbook exists offline and was used in the last exercise.

## Checked
2026-10-28. Confirmed against the restic docs (`--exclude-caches`, `--read-data-subset`, `forget --keep-* --prune`, `RESTIC_REPOSITORY`, `RESTIC_PASSWORD_FILE`, S3 repository URL form, `restore --target --include`, `--tag`, rest-server `--append-only`), the BorgBackup usage pages (`init`, `create --stats`, `prune`, `compact`, `check`, `serve --append-only`, `key export`, `repokey-blake2`, `{hostname}-{now}`) and the AWS S3 Object Lock page (compliance versus governance mode). Removed: the DB dump command flags, the 30-day history figure, the Proxmox retention-lock claim and the SureBackup name. The 3-2-1-1-0 rule and the example tiers are conventions with no readable source (the CISA page returned 403), so they stay marked as unconfirmed.
Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.virtualisation.proxmox-backup-server-storage-entry
name: proxmox-backup-server-storage-entry
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pbs-storage-entry, proxmox-backup-server, pvesm, proxmox, backup]
level: practitioner
status: docs-checked
description: "Add a Proxmox Backup Server datastore as PVE storage with API tokens, fingerprint, namespaces and client-side encryption, and protect the encryption key."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#storage_pbs
  - https://pbs.proxmox.com/docs/
  - https://github.com/proxmox/pve-docs/blob/master/pve-storage-pbs.adoc
  - https://github.com/proxmox/pve-storage/blob/master/src/PVE/Storage/PBSPlugin.pm
  - https://github.com/proxmox/proxmox-backup/blob/master/docs/user-management.rst
  - https://github.com/proxmox/proxmox-backup/blob/master/docs/backup-client.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox Backup Server as a storage entry

**Goal:** PVE backs up to PBS with deduplication, encryption and least-privilege credentials.

## On PBS
1. Create a datastore (`store1`) and optionally a namespace per cluster (`pve-prod`).
2. Create a user and API token, for example `pve-backup@pbs!pve1`, and grant `DatastoreBackup` on `/datastore/store1` (`DatastoreBackup` can back up and restore owned backups; `DatastorePowerUser` can also prune owned backups, so add it only if PVE should prune).
3. Note the certificate fingerprint: from the server's dashboard, or with `proxmox-backup-manager cert info`. It is required for self-signed certificates or any certificate the PVE host does not trust.

## On PVE
```bash
pvesm add pbs pbs-store1 --server pbs.example.com --datastore store1 --namespace pve-prod \
  --username 'pve-backup@pbs!pve1' --password '<token-secret>' \
  --fingerprint 'aa:bb:...:ff' --encryption-key autogen --content backup
```
GUI: Datacenter -> Storage -> Add -> Proxmox Backup Server.

## Encryption key
`--encryption-key autogen` generates a key (`proxmox-backup-client key create --kdf none`) stored at `/etc/pve/priv/storage/pbs-store1.enc`, readable only by root; only keys without a password (no KDF) are supported. Encryption is client-side AES-256 in GCM mode. Backups are inaccessible without the key, so keep copies away from the systems being backed up (password manager, USB drive, paper): `proxmox-backup-client key paperkey /etc/pve/priv/storage/pbs-store1.enc --output-format text > qrkey.txt`. Optionally set `master-pubkey` so each encrypted backup carries an RSA-encrypted copy of the key for recovery. Deduplication between backups made with different keys is not possible.

## Pruning
The storage supports the common `prune-backups` property (PVE-side retention); retention can also be handled by prune jobs on the PBS side. Choose one place to own retention.

## Gotchas
- Use `<user>@<realm>` (or an API token ID such as `user@pbs!token`) as `username`; the guide's TIP says not to forget the realm. The password is saved in `/etc/pve/priv/storage/<id>.pw`, readable only by root.
- Fingerprint changes when the PBS certificate is replaced; update the storage entry or backups fail with TLS errors.
- Network: the default PBS port is 8007 (the `port` property overrides it); every PVE node must reach it.

## Verify
`pvesm status` shows the PBS storage active; a test backup completes, and the snapshot shows *Encrypted* in PBS.

## Checked

Docs: Proxmox VE admin guide sources (proxmox/pve-docs, master, last commit 2026-10-17) and storage plugin sources (proxmox/pve-storage, master, last commit 2026-10-09). Proxmox Backup Server docs (proxmox/proxmox-backup, docs/user-management.rst and docs/backup-client.rst).

Confirmed: `server`, `port` (default 8007), `username` with realm, `datastore`, `fingerprint` (needed for self-signed certificates; shown in the dashboard or by `proxmox-backup-manager cert info`), `encryption-key` including `autogen` and the `.enc` path, `master-pubkey`, `namespace` and `prune-backups` support in the plugin source, password file location, AES-256 GCM client-side encryption, paperkey command, no dedup across keys, backup-only content type; PBS role descriptions for DatastoreBackup and DatastorePowerUser. The PBS client documentation says its password variable can be set to an API token secret; the PVE storage page itself documents only a user password, so test the token login after adding the storage. The draft's statement that the token secret is shown only once was removed as unconfirmed.

Method: documentation only; no commands were run.

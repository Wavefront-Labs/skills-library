---
id: computing-software.systems-network-administration.backup-and-recovery.pbs-client-side-encryption-and-master-key
name: pbs-client-side-encryption-and-master-key
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pbs-encryption, proxmox-backup-server, backup-encryption, key-escrow, proxmox-backup-client, proxmox]
level: advanced
status: docs-checked
description: "Encrypt Proxmox backups client-side for PBS: create keys on PVE storage or the client, master key for recovery, paperkey escrow, and what happens if the key is lost."
sources:
  - https://pbs.proxmox.com/docs/backup-client.html
  - https://pve.proxmox.com/pve-docs/chapter-pvesm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PBS client-side encryption and master key

PBS encryption is **client-side**, AES-256 in GCM mode: the key stays with the client (Proxmox VE or `proxmox-backup-client`).

## On Proxmox VE (storage-level key)
Datacenter, Storage, (PBS storage), Encryption: generate a key or upload one. CLI:
```sh
pvesm set pbs01 --encryption-key autogen
```
The key is saved in `/etc/pve/priv/storage/<STORAGE-ID>.enc`, readable only by root. The value `autogen` generates a new key (passphrase-less keys are supported). The storage option `master-pubkey`, which requires `encryption-key`, appends the key, encrypted with the master public key, to each backup on the PBS server for recovery.

## On a standalone client
```sh
proxmox-backup-client key create my-backup.key                  # passphrase-protected
proxmox-backup-client key create /path/to/my-backup.key --kdf none   # for unattended use
proxmox-backup-client backup etc.pxar:/etc --keyfile /path/to/my-backup.key
```
Without a name the key goes to the default `~/.config/proxmox-backup/encryption-key.json`, which the client also searches when `--keyfile` is omitted.

## Master key (recover lost client keys)
```sh
proxmox-backup-client key create-master-key          # creates master-public.pem and master-private.pem
proxmox-backup-client key import-master-pubkey /path/to/master-public.pem   # on each client
```
With the public key imported, the client stores a copy of its encryption key, encrypted with the master key, alongside each backup. To recover, decrypt the stored key with the private master key:
```sh
proxmox-backup-client key import-with-master-key /path/to/target \
  --master-keyfile /path/to/master-private.pem --encrypted-keyfile /path/to/rsa-encrypted.key
```
Keep the master private key safe but quickly reachable (the docs suggest a password manager) plus a printed paper copy.

## Escrow
```sh
proxmox-backup-client key paperkey /etc/pve/priv/storage/<STORAGE-ID>.enc --output-format text > qrkey.txt
```
Print it and store it safely. Without the key (or the master key route) encrypted backups cannot be decrypted.

## Gotchas
- The PVE key file lives under `/etc/pve/priv`, so losing the cluster loses the key unless it was escrowed.

## Verify
Do a test restore on a fresh node using only the paperkey-recovered or master-key-recovered key.

## Checked
2026-10-28. Confirmed against the PBS client page (AES-256 GCM, `key create`, `--kdf none`, `--keyfile`, default key location, `create-master-key`, `import-master-pubkey`, `import-with-master-key`, `paperkey`) and the PVE storage chapter (`encryption-key`, `autogen`, `.enc` path, `master-pubkey`). Removed because the pages do not state them: the claims about deduplication under one key, sync and verify behaviour with encrypted chunks, key changes and the lock icon, and the invented `key restore` command.
Method: documentation only; no commands were run.

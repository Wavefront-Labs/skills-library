---
id: computing-software.systems-network-administration.backup-and-recovery.backup-password-and-key-storage
name: backup-password-and-key-storage
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-password-storage, key-escrow, backup-encryption, password-loss-protection, break-glass, disaster-recovery]
level: practitioner
status: draft
description: "Store backup encryption passwords and keys so they survive the disaster: offline escrow, sealed envelopes, split knowledge, vault replicas outside production, and access tests."
sources:
  - https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
  - https://helpcenter.veeam.com/docs/backup/vsphere/encryption_keys.html?ver=120
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Storing backup passwords and keys

Encrypted backups without their key are random data. The classic failure: the key lived in
the password manager hosted on the infrastructure that just burned down or got encrypted.

## What to protect
- Backup job/repository encryption passwords (Veeam job passwords, restic repo passwords,
  PBS encryption keys and master key, Bacula/TDE certificates).
- Backup server configuration backup password (Veeam config backup encryption).
- Cloud KMS access paths and break-glass credentials for backup accounts.
- Credentials for immutable storage consoles, tape/vault vendors.

## Storage pattern
1. **Primary**: enterprise vault (HashiCorp Vault, CyberArk, Bitwarden/1Password business)
   with a replica or export **outside** the production identity and infrastructure.
2. **Offline escrow**: printed or on hardware tokens, in sealed tamper-evident envelopes in a
   safe at two locations (office + offsite/bank/DR site). Record envelope serials.
3. **Split knowledge** for the most sensitive keys (two people each hold half, or Shamir
   secret sharing like `ssss`/Vault unseal keys) so no single insider can decrypt.
4. Document **who can access** each copy and how (call tree), in the DR plan.

## Product notes
- Veeam: enable **Password loss protection** via Enterprise Manager (key sets) so lost job
  passwords can be recovered; still escrow passwords.
- PBS: back up the client encryption key and create a **master key** (RSA) to recover
  per-client keys; paperkey output (`proxmox-backup-client key paperkey`) for printing.
- restic: no recovery without a password; add a second key (`restic key add`) held in escrow.

## Test
Annually (and after rotation): a person who doesn't normally do backups retrieves the
escrowed key from the offline copy and restores a test dataset on an isolated machine.

## Gotchas
- Rotation without updating escrow = trap; make escrow update part of the rotation procedure.
- Printed passwords with ambiguous characters (O/0, l/1): use a font/encoding that avoids
  them or include a checksum.

## Verify
Escrow register lists every key, its copies and last test date; last test restore succeeded
using only offline material.

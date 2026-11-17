---
id: computing-software.systems-network-administration.backup-and-recovery.lto-hardware-encryption
name: lto-hardware-encryption
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [lto-encryption, tape-encryption, aes-256-gcm, kmip, application-managed-encryption, ltfs]
level: advanced
status: draft
description: "Encrypt LTO tapes with drive-based AES-256: application-, library- and system-managed key modes, KMIP key managers, Veeam tape encryption and restore-elsewhere planning."
sources:
  - https://www.lto.org/technology/
  - https://www.ibm.com/docs/en/ts4500-tape-library?topic=encryption-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LTO hardware encryption

LTO-4 and later drives encrypt with AES-256-GCM in the drive at full speed, after compression, so there is no throughput or capacity penalty.

## Key management modes
| Mode | Who supplies keys | Typical use |
|---|---|---|
| **Application-managed (AME)** | Backup software (Veeam, Bacula, NetBackup) | Most common; keys in backup software |
| **Library-managed (LME)** | Library talks to a KMIP key manager | Central policy, many backup apps |
| **System-managed (SME)** | Host driver/OS | Mainframe/IBM environments |

## Veeam tape encryption
- Media pool > Options > Enable encryption; choose a password or KMS key. With hardware encryption-capable drives, Veeam uses drive encryption; otherwise it encrypts in software.
- Enterprise Manager key loss protection allows decrypting with the EM recovery key if the password is lost.
- Catalog the tapes in a new Veeam server: you need the password to read them.

## Library-managed with KMIP
Configure the library's encryption settings: KMIP server addresses (port 5696), certificates, key group; enable encryption per logical library/partition. Backup software is unaware.

## Planning restore elsewhere
- Off-site or vaulted tapes must be readable at the DR site: same drive generation (LTO drives read two generations back on LTO-7 and earlier, one back on LTO-8 and later), key access, backup catalog or the ability to re-catalog.
- Keep key escrow (KMS replication or sealed password records) separate from the tapes.

## Gotchas
- Mixed encrypted/unencrypted pools confuse operators; label pools clearly.
- Losing the key = tapes are scrap. Test a restore on a different drive with keys from escrow.

## Verify
`sg_logs` or library UI shows encryption enabled for tapes; a restore at the DR site from a vaulted tape succeeds with escrowed keys.

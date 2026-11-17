---
id: computing-software.cryptography-implementation.key-management.hsm-and-token-zeroization
name: hsm-and-token-zeroization
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, hsm-zeroization, zeroization, hsm, decommissioning, rma, yubihsm, softhsm, pkcs11, key-destruction, fips-140-3]
level: practitioner
status: draft
description: "Zeroize HSMs, smart cards and tokens before decommissioning, RMA or after compromise: vendor procedures, partition versus full reset, evidence and backups."
sources: ["https://csrc.nist.gov/pubs/fips/140-3/final", "https://csrc.nist.gov/pubs/sp/800/88/r1/final", "https://docs.yubico.com/hardware/yubihsm-2/hsm-2-user-guide/hsm2-cmd-reference.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HSM and token zeroization

FIPS 140-3 requires modules to provide a way to zeroise all unprotected sensitive security parameters (SSPs). Your
procedure must use it, prove it happened, and make sure no copy survives elsewhere.

## Scope first
| Action | Destroys |
|---|---|
| Delete key object | One key (backups may still hold it) |
| Partition/slot reinitialise | All keys in that partition |
| Full zeroise / factory reset | All keys, users, policies on the device |
| Physical destruction | Device (after zeroise) |

## Procedures by type (check your firmware docs)
- **Network HSMs (Thales Luna, Entrust nShield, Utimaco):** use the vendor's zeroise/factory-reset command from the
  admin shell or tamper button; also delete partitions from HA groups and destroy backup tokens or backup HSMs that
  hold the same keys.
- **YubiHSM 2:** `yubihsm-shell -a reset` (or physical reset on insertion) wipes all objects.
- **PKCS#11 tokens / smart cards:** `pkcs11-tool --init-token --label new --so-pin <SO-PIN>` destroys token objects;
  PIV cards: `ykman piv reset` (after PIN/PUK blocked) wipes PIV keys.
- **SoftHSM2:** `softhsm2-util --delete-token --token <label>`, then securely delete the token directory.
- **Cloud HSM (AWS CloudHSM, Azure Managed HSM):** delete keys, then the cluster/HSM, and the retained backups (check
  backup retention settings; backups outlive the cluster by default).

## Evidence
- Two-person execution; record device serial, date, command output, and post-reset status showing no objects.
- Update the key inventory: state Destroyed (or Destroyed-Compromised), date, witness.

## Gotchas
- Backup tokens and HA peers are the usual surviving copy.
- RMA'd devices must be zeroised before shipping; tamper-zeroised devices may need vendor re-initialisation.
- Wrapped key blobs stored outside the HSM become useless only once the wrapping key is zeroised; confirm which keys
  wrapped them.

## Verify
- [ ] Post-zeroise listing shows no objects/partitions.
- [ ] Backups holding the same keys are destroyed or re-scoped.

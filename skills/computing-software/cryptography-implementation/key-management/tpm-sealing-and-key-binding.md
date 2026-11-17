---
id: computing-software.cryptography-implementation.key-management.tpm-sealing-and-key-binding
name: tpm-sealing-and-key-binding
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-storage, tpm-sealing, tpm2, pcr-policy, tpm2-tools, systemd-cryptenroll, clevis, measured-boot]
level: advanced
status: draft
description: "Seal secrets to a TPM 2.0 with PCR policies so they unlock only on the expected boot chain: tpm2-tools and systemd-cryptenroll recipes, PCR choice, and update breakage."
sources: ["https://trustedcomputinggroup.org/resource/tpm-library-specification/", "https://tpm2-tools.readthedocs.io/en/latest/", "https://www.freedesktop.org/software/systemd/man/latest/systemd-cryptenroll.html", "https://uapi-group.org/specifications/specs/linux_tpm_pcr_registry/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TPM sealing and key binding

A TPM 2.0 can seal a secret (a disk key, an API credential) so it is released
only when Platform Configuration Registers (PCRs) match expected values, i.e.
the machine booted the expected firmware, bootloader and kernel. Stolen disks
cannot be unlocked elsewhere, and a tampered boot chain cannot unlock them.

## Disk unlock (most common)

```bash
# LUKS2 + systemd: bind to Secure Boot state (PCR 7), optionally PIN
systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=7 --tpm2-with-pin=yes /dev/nvme0n1p3
# /etc/crypttab: luks-root UUID=... none tpm2-device=auto
# Clevis alternative
clevis luks bind -d /dev/nvme0n1p3 tpm2 '{"pcr_bank":"sha256","pcr_ids":"7"}'
```

Keep a recovery passphrase or recovery key slot (`systemd-cryptenroll --recovery-key`).

## Sealing an arbitrary secret

```bash
tpm2_createprimary -C o -c prim.ctx
tpm2_pcrread sha256:0,7 -o pcr.bin
tpm2_createpolicy --policy-pcr -l sha256:0,7 -f pcr.bin -L pcr.policy
tpm2_create -C prim.ctx -L pcr.policy -i secret.bin -u seal.pub -r seal.priv
# later
tpm2_load -C prim.ctx -u seal.pub -r seal.priv -c seal.ctx
tpm2_unseal -c seal.ctx -p pcr:sha256:0,7
```

`seal.priv` is encrypted under the TPM's storage hierarchy and useless on
another TPM. For servers, `systemd-creds encrypt --with-key=tpm2` wraps service
credentials the same way.

## Choosing PCRs

| PCR | Measures | Changes when |
|---|---|---|
| 0 | firmware code | BIOS/UEFI update |
| 2 | option ROMs | GPU/NIC firmware update |
| 4 | boot loader | bootloader or kernel (UKI) update |
| 7 | Secure Boot policy (db/dbx, keys) | Secure Boot key or dbx update |
| 11 | systemd-stub UKI sections | every kernel update |

Binding many PCRs is stronger but breaks on every update. Common choice: PCR 7
alone (trust the Secure Boot signer). For tighter binding without update
pain, use signed PCR policies (`systemd-measure` + `--tpm2-public-key`), so a
vendor-signed new kernel still unlocks.

## Pitfalls

- Firmware or dbx update makes the secret unrecoverable without the fallback.
  Re-seal after updates or use signed policies.
- TPM sealing does not stop an attacker with the running, unlocked machine.
- Add a PIN (`--tpm2-with-pin`) against evil-maid with stolen whole laptops;
  TPM dictionary-attack lockout limits guessing.
- Bus sniffing on discrete TPMs (LPC/SPI) can capture unsealed secrets; use
  parameter encryption (sessions) - systemd and clevis do.

## Verify

- [ ] Boot with Secure Boot disabled or modified bootloader: unlock fails.
- [ ] Recovery key works on a test restore.
- [ ] Update procedure tested (firmware, kernel) without lockout.

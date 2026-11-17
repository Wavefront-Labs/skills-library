---
id: computing-software.digital-privacy-hygiene.device-hardening.secure-boot-firmware-and-evil-maid-defense
name: secure-boot-firmware-and-evil-maid-defense
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, secure-boot, uefi, bios, tpm, tpm2, evil-maid, firmware-attack, bitlocker-pin, bootguard, measured-boot, dma-protection, kernel-dma-protection, firmware-password, thunderspy, pcileech, bootkit, chain-of-trust, pin-at-boot, uefi-password]
level: advanced
status: draft
description: "Harden UEFI/Secure Boot, TPM and firmware settings against evil-maid and bootkit attacks: set a firmware password, enable measured boot, add a pre-boot PIN, block DMA."
sources:
  - "https://learn.microsoft.com/en-us/windows/security/information-protection/bitlocker/bitlocker-countermeasures"
  - "https://tpm.fail/"
  - "https://safeboot.dev/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure Boot, firmware and evil-maid defense

**Goal:** make brief unsupervised physical access to a locked laptop (a hotel room,
airport security, a border stop) worthless to an attacker who wants to plant a
bootkit, sniff a disk key, or dump memory — not just deter casual snooping.

## 1. What "evil maid" actually means
Disk encryption (`computing-software.digital-privacy-hygiene.device-hardening.personal-device-hardening-checklist`)
protects data at rest when the machine is off. It does nothing if an attacker can
briefly boot a tampered OS, modify the bootloader, or install a hardware keylogger
before you type your password again — the next unlock hands over the key. Evil-maid
defense closes that specific gap between "encrypted" and "actually safe unattended."

## 2. Secure Boot and the chain of trust
- Confirm **Secure Boot is On** (Windows: `msinfo32` → Secure Boot State; or
  Settings → Privacy & security → Device security → Core isolation → Memory
  integrity page also shows it). It only works with UEFI mode, not legacy BIOS/CSM.
- **Set a firmware (BIOS/UEFI) supervisor password.** Without one, anyone with
  physical access can disable Secure Boot, change the boot order, or boot a USB
  "maintenance" OS in under a minute. This is the single highest-value step here
  and is skipped constantly.
- On Windows with a TPM, enable **measured boot**: TPM PCR values capture
  bootloader/firmware hashes at startup; BitLocker can be bound to them so a
  modified boot chain fails to auto-unlock instead of silently succeeding.

## 3. Add a pre-boot factor to disk encryption
- **Windows/BitLocker**: `manage-bde -protectors -add C: -TPMAndPIN` adds a PIN the
  TPM demands before release, defeating "cold boot with TPM sniffed over LPC/SPI bus"
  attacks that plagued discrete (non-fTPM) TPMs. Modern CPUs with fTPM/PTT integrated
  into the chipset are far less exposed to bus-sniffing than older discrete TPM chips,
  but a PIN still adds a factor independent of the disk itself.
- **macOS/FileVault**: there is no separate pre-boot PIN option; rely on a strong
  login password plus a firmware password (`firmwarepasswd` via Recovery, or on
  Apple Silicon this is largely superseded by the Secure Enclave's own boot chain).
- **Linux/LUKS**: use a passphrase, not just a TPM-auto-unlock keyfile, if the threat
  model includes device theft; TPM-only unlock without a passphrase is convenience,
  not evil-maid resistance.

## 4. Kernel DMA / Thunderbolt protection
Thunderbolt and some USB-C ports allow direct memory access that has been used
(Thunderspy, 2020) to bypass lock screens and extract keys in minutes with physical
access, including some BitLocker-protected machines. Windows 10 2004+/11: Settings →
Privacy & security → Device security → Core isolation, or check **Kernel DMA
Protection** via `msinfo32`. It requires IOMMU/VT-d support and is only fully
effective when enabled from first boot (enabling it later still helps but a
determined attacker who had earlier access had a window). On machines without it,
disable unused Thunderbolt ports in firmware when traveling, or use **Bootguard/
Thunderbolt security level "User Authorization"** in firmware settings where offered.

## 5. Travel and border-crossing posture
- Fully shut down (not sleep/hibernate) before anything leaves your sight — a
  running or sleeping machine's keys often live in RAM, reachable by cold-boot or
  DMA attacks that a powered-off, encrypted disk defeats entirely.
- Consider a travel-only account/device with minimal data for border crossings where
  device search or compelled unlock is a real risk; policies vary enormously by
  country and I can't give legal advice on refusal consequences — check a current
  source (e.g. EFF's border search guidance) for your situation.
- Tamper-evidence (a seal over ports, a bag with a numbered tie) is a detection
  measure, not a prevention one — pair it with the above, don't rely on it alone.

## Gotchas
- A firmware password without Secure Boot, or Secure Boot without a firmware
  password, each leave the other half of the gap open — do both together.
- Some OEM firmware lets Secure Boot be disabled from the OS with no password at
  all; verify after setting the password by attempting the change yourself.
- Uncertain: exact Thunderbolt security-level naming and IOMMU exposure differ by
  OEM and CPU generation — verify on the specific model.

## Verify
- [ ] Firmware supervisor password set; disabling Secure Boot now requires it.
- [ ] Secure Boot confirmed On (`msinfo32` or equivalent).
- [ ] Disk encryption bound to a PIN or passphrase, not silent TPM-only auto-unlock.
- [ ] Kernel DMA Protection / IOMMU confirmed on, or unused Thunderbolt/USB-C ports
      disabled before travel.
- [ ] Machine is fully powered off, not sleeping, whenever it leaves your control.

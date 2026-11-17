---
id: computing-software.cybersecurity-defensive.system-hardening.tpm-measured-boot-attestation
name: tpm-measured-boot-attestation
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [firmware-security, measured-boot, tpm, remote-attestation, pcr, device-health-attestation, keylime]
level: sme
status: draft
description: "Use TPM measured boot and remote attestation: understand PCRs and event logs, enable Windows device health attestation, bind secrets to PCRs and run Keylime on Linux."
sources: ["Trusted Computing Group - TPM 2.0 Library Specification and PC Client Platform Firmware Profile", "Microsoft Learn - Measured Boot and Device Health Attestation", "Keylime project documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TPM measured boot and attestation

**Goal:** prove remotely that a host booted known-good firmware, bootloader and kernel, and gate access or secrets on that proof.

## Concepts
- Each boot stage hashes the next into TPM Platform Configuration Registers (PCRs) via extend operations; the event log (`/sys/kernel/security/tpm0/binary_bios_measurements`, Windows TCG logs in `%WINDIR%\Logs\MeasuredBoot`) records what was measured.
- Typical PCRs: 0 firmware code, 1 firmware config, 2-3 option ROMs, 4 boot manager, 7 Secure Boot policy (keys/dbx state), 8-9 kernel/initrd (GRUB/systemd-boot), 11 unified kernel image (systemd-stub).
- Attestation: TPM signs a quote of PCR values with an attestation key (AK) chained to its endorsement key (EK); a verifier replays the event log and compares against policy.
- Secure Boot enforces; measured boot records. They complement each other.

## Windows
- Device Health Attestation is used by Intune compliance ("Require BitLocker", "Require Secure Boot", "Require code integrity") and Defender for Endpoint.
- BitLocker seals its key to PCR 7 + 11 (with Secure Boot) - a changed boot chain prompts for recovery.
- `Get-Tpm`, `tpm.msc`; TPM 2.0 required for Windows 11.

## Linux
- Inspect: `tpm2_pcrread sha256:0,1,4,7,8,9`, `tpm2_eventlog /sys/kernel/security/tpm0/binary_bios_measurements`.
- Bind disk unlock to PCRs: `systemd-cryptenroll --tpm2-device=auto --tpm2-pcrs=7 /dev/nvme0n1p3` (use signed PCR policies with UKIs (`--tpm2-public-key`) to survive kernel updates).
- Keylime: agent on host, verifier/registrar central; policies for measured boot (event log reference state) and IMA runtime integrity; revocation actions when attestation fails.

## Operations
- Firmware and bootloader updates change PCRs; update reference values in the verifier or BitLocker/LUKS policy before rollout, or suspend sealing for the update (`Suspend-BitLocker -RebootCount 1`).
- Store EK certificates/hashes at enrolment to prevent swapped TPM or software TPM impersonation.

## Verify
- [ ] Attestation dashboard shows all enrolled hosts passing; failures generate tickets.
- [ ] A test boot with Secure Boot disabled changes PCR 7 and fails attestation / triggers BitLocker recovery.

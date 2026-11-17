---
id: computing-software.digital-privacy-hygiene.device-hardening.checking-tpm-status
name: checking-tpm-status
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, tpm-status, tpm2, firmware-tpm]
level: practitioner
status: docs-checked
description: "Check whether a PC's TPM 2.0 is present on Windows and Linux, and find the firmware switch (Intel PTT, AMD fTPM) when it is missing."
sources:
  - "https://support.microsoft.com/windows/enable-tpm-2-0-on-your-pc-1fd5a332-360d-4f46-a1e7-ae6b0c90645c"
  - "https://www.freedesktop.org/software/systemd/man/latest/systemd-cryptenroll.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Checking TPM status

**Goal:** know whether disk encryption and Windows Hello have a working TPM underneath.

## Windows
- Run `tpm.msc`: it confirms the TPM is ready, and under TPM Manufacturer Information the Specification Version
  field should read 2.0. If it says a compatible TPM cannot be found, the TPM is likely disabled in firmware.
- Windows Security > Device security > **Security processor details**: check that Specification version is 2.0.
  If there is no Security processor section, the TPM may be disabled.

## Linux
`systemd-cryptenroll --tpm2-device=list` enumerates the suitable TPM2 devices it discovers. An empty list means
none was found.

## Not present? Enable in firmware
In UEFI setup, look for the labels Microsoft lists: Intel PTT / Intel Platform Trust Technology, AMD fTPM /
AMD PSP fTPM, "Security Device" or "TPM State". Save and reboot, then recheck.

## Clearing the TPM
Do not clear a TPM unless Microsoft's or your device maker's instructions tell you to; read their guidance first,
and back up any disk-encryption recovery keys beforehand.

## Gotchas
- `systemd-cryptenroll` can require a PIN as well as TPM binding with `--tpm2-with-pin`; it defaults to no.

## Checked
2026-11-01. Confirmed against Microsoft's "Enable TPM 2.0" page: tpm.msc and Windows Security checks for version
2.0, "compatible TPM cannot be found" meaning, firmware setting names. Confirmed against the systemd-cryptenroll
man page: `--tpm2-device=list` and `--tpm2-with-pin` (default no). Removed as unconfirmed: exact tpm.msc status
text, Get-Tpm output, /dev/tpm and sysfs checks, clearing consequences (Microsoft's page has no such warning),
AMD BIOS-update reset claim, BitLocker PIN claim and the Learn URL (not read).
Method: documentation only; no commands were run.

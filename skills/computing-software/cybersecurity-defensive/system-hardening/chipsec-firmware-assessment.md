---
id: computing-software.cybersecurity-defensive.system-hardening.chipsec-firmware-assessment
name: chipsec-firmware-assessment
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [chipsec, firmware-security, uefi, spi-flash, bios-write-protection, platform-security]
level: advanced
status: docs-checked
description: "Assess platform firmware security with CHIPSEC: running module checks for SPI flash and BIOS write protection, SMM locks and Secure Boot, dumping firmware, and baselining."
sources: ["https://github.com/chipsec/chipsec", "https://chipsec.github.io/", "https://csrc.nist.gov/pubs/sp/800/147/final", "https://csrc.nist.gov/pubs/sp/800/193/final", "https://chipsec.github.io/usage/Running-Chipsec.html", "https://chipsec.github.io/modules/chipsec.modules.common.bios_wp.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CHIPSEC firmware assessment

CHIPSEC (open source) tests x86 platform configuration for firmware protections: whether the
BIOS/UEFI region can be rewritten from the OS, whether SMM is locked, and more. Use it to evaluate hardware
models before purchase, verify vendor firmware updates, and investigate suspected firmware implants.

## Setup
CHIPSEC runs on Windows, Linux and the UEFI shell and must be launched as Administrator/root. Its documentation
says to use it only on test systems, not production end-user systems: the kernel driver gives user-mode code direct
hardware access, on Windows it needs TestSigning mode (which turns off a kernel protection), and a module that
misuses hardware can hang the OS.
```bash
python setup.py build_ext -i      # run in place without installing
sudo python chipsec_main.py       # runs applicable modules
sudo python chipsec_main.py -m common.bios_wp
```

## Key modules
- `common.bios_wp`: BIOS region write protection, via SMM-based protection (BIOS Control register WPD/BIOSWE,
  BLE and EISS/SMM_BWP bits) or SPI Protected Range registers PR0-PR4 covering the whole BIOS region. It fails if
  SMM protection is not correctly configured and the PR registers do not protect the entire region.
- `common.spi_lock`: SPI flash controller configuration (including PR0-PR4) locked by HSFS[FLOCKDN].
- `common.spi_desc`: software cannot write to the flash descriptor.
- `common.smm`: SMRAMC[D_LCK] set; `common.smrr`: SMRRs enabled and configured.
- `common.secureboot.variables`: Secure Boot key UEFI variables are authenticated and protected from modification
  (`-a modify` tries to write them, so use it only on test systems).
- `common.me_mfg_mode`: ME Manufacturing mode is not enabled.
Read each module's documentation page for platform-specific caveats.

## Firmware dump and comparison
`chipsec_util.py` provides SPI and UEFI commands (run `python chipsec_util.py --help` for the list in your version).
Dump the firmware and compare it against the vendor's firmware image or a known-good dump from the same
model/version (hash the BIOS region; diff extracted module lists) to look for added or changed modules.

## Using results
- FAILED write protection on current firmware: raise with the vendor, update firmware, or choose another
  model; NIST SP 800-147/800-193 define expected protections (authenticated updates, protection, detection,
  recovery).
- Record results per hardware model and firmware version as part of the platform baseline.

## Gotchas
- A FAILED result can be a platform that implements protection differently; confirm with the vendor.
- Module coverage varies by platform; check which modules run on yours.
- Never write to SPI flash unless recovering under a controlled process.

## Verify
For each approved hardware model, a stored CHIPSEC report shows bios_wp, spi_lock and smm passing on the
deployed firmware version.

## Checked
2026-10-31. Confirmed on chipsec.github.io: supported environments, run-as-root, the test-systems-only warning and its reasons, `chipsec_main.py -m`, `python setup.py build_ext -i`, and the module pages for bios_wp, spi_lock, spi_desc, smm, smrr, secureboot.variables and me_mfg_mode. Removed: bios_kbrd_buffer, bios_ts and CPU vulnerability modules, the result-label list, named firmware implants, the AMD coverage claim, and exact `chipsec_util` command forms (not confirmed on a fetched page).
Method: documentation only; no commands were run.

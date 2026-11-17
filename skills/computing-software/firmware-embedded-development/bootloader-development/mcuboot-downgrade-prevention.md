---
id: computing-software.firmware-embedded-development.bootloader-development.mcuboot-downgrade-prevention
name: mcuboot-downgrade-prevention
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [downgrade-prevention, mcuboot, security-counter, hw-rollback-protection, version-compare, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Stop MCUboot installing older images: version checks vs hardware security counters, imgtool --security-counter, and the Zephyr Kconfig options that enable each."
sources:
  - https://docs.mcuboot.com/design.html
  - https://docs.mcuboot.com/imgtool.html
  - https://raw.githubusercontent.com/mcu-tools/mcuboot/main/boot/zephyr/Kconfig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Downgrade prevention

An attacker (or a confused update server) installing an older, validly signed image with a
known vulnerability defeats secure boot. MCUboot offers two mechanisms; the design doc says the
new image must have a higher version or security counter than the one it replaces.

## 1. Software downgrade prevention (version compare)
Enabled with `MCUBOOT_DOWNGRADE_PREVENTION`; in Zephyr `CONFIG_MCUBOOT_DOWNGRADE_PREVENTION=y`
in the MCUboot image config (not available with `BOOT_DIRECT_XIP`).
- Zephyr Kconfig help: an upgrade must have a greater major version, or a greater minor version
  with an equal major version. By default the comparison uses only major, minor and revision;
  `CONFIG_BOOT_VERSION_CMP_USE_BUILD_NUMBER` adds the build number.
- MCUboot's design doc states the software check is available only with the overwrite-based
  strategy (`MCUBOOT_OVERWRITE_ONLY`); Zephyr's Kconfig and sysbuild docs also describe it for
  swap modes (the main app then selects `MCUBOOT_BOOTLOADER_NO_DOWNGRADE`). Check your MCUboot
  version.
- The comparison uses the version in the signed header: set it with
  `imgtool sign --version 1.4.2+7` (the `+N` part is the build number).
- The Kconfig help warns it only protects against some attacks: a JTAG could be used to write
  an older version.

## 2. Hardware rollback protection (security counter)
Each signed image can carry a security counter in its protected TLV area (`imgtool sign -s` /
`--security-counter`; the `auto` keyword derives it from the image version). The new image's
counter is compared with the active counter stored in a non-volatile, trusted component of the
device. Enable with `MCUBOOT_HW_ROLLBACK_PROT`; the target must implement the security counter
interface in `boot/bootutil/include/security_cnt.h`. Zephyr Kconfig: `MCUBOOT_HW_DOWNGRADE_PREVENTION`.
```sh
imgtool sign ... --security-counter 3 app.bin app.signed.bin
```
- The counter is handled independently of the version: it need not increase with each release,
  and an older image with the **same** counter value is still accepted (so some software
  downgrade remains possible).
- `MCUBOOT_HW_DOWNGRADE_PREVENTION_COUNTER_LIMITED` (counter has a limited number of updates):
  MCUboot checks whether the counter can still be updated and rejects the update if it cannot.
  `MCUBOOT_HW_DOWNGRADE_PREVENTION_LOCK` locks counter updates before the application boots.
- `MCUBOOT_DOWNGRADE_PREVENTION_SECURITY_COUNTER` makes the swap-mode eligibility check use the
  security counter instead of the version.

## Choosing
| Need | Mechanism |
|---|---|
| Prevent accidental downgrades during development | version-based |
| Security requirement (e.g. after a CVE fix) | hardware security counter |
| Allow legitimate rollback to recent versions | security counter, raised only on security fixes |

## Operational notes
- A downgrade request from the update server should fail with a clear "older version" result
  instead of being retried forever.
- Test the counter update path with a reverted image before shipping.

## Verify
- [ ] Uploading an older signed image: MCUboot keeps the current image.
- [ ] After an update with a higher security counter, images below that counter no longer boot.

## Checked
2026-10-31. Confirmed against the MCUboot design doc (Downgrade prevention, security counter TLV, `-s`,
`MCUBOOT_HW_ROLLBACK_PROT`, `security_cnt.h`), the imgtool page (`--version`, `--security-counter` with `auto`) and
MCUboot `boot/zephyr/Kconfig` (option names, major/minor rule, counter-limited/lock/security-counter options, JTAG
caveat). Fixed: the version rule is major/minor (not revision) per Kconfig help. Removed: the hardware counter
function names, OTP increment counts, the TF-M claim, per-image counters, and the claim that the counter bump timing
can leave no bootable image.
Method: documentation only; no commands were run.

---
id: computing-software.firmware-embedded-development.bootloader-development.firmware-image-versioning-policy
name: firmware-image-versioning-policy
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [image-version, ab-update, semantic-versioning, security-counter, compatibility-matrix, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Define firmware versions for update logic: semantic version vs build number vs security counter, comparison rules, hardware compatibility IDs, header fields."
sources:
  - https://semver.org/
  - https://docs.mcuboot.com/imgtool.html
  - https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/system/ota.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image versioning policy

Versions drive decisions: whether an update is offered, whether a downgrade is allowed, which
image a bootloader prefers, and which hardware it may run on. Mixing these purposes in one number
causes trouble.

## Three different numbers
| Number | Purpose | Example |
|---|---|---|
| **Product version** (semantic) | human/marketing, release notes, compatibility of APIs | 2.4.1 |
| **Build number / monotonic version** | strictly increasing per release for "newer than" comparisons | 2041, or MCUboot `2.4.1+17` (build field) |
| **Security counter** | anti-rollback: only increases when a vulnerability fix must never be undone | 3 |
MCUboot image header carries `ih_ver` (major, minor, revision, build number) and optionally a
security counter (`imgtool sign --security-counter`). ESP-IDF stores a `secure_version` in
`esp_app_desc_t` for anti-rollback (compared with the version in eFuse).

## Comparison rules
- Compare numerically per field, never as strings ("2.10.0" < "2.9.0" as strings; SemVer
  requires major, minor and patch to be compared numerically).
- Decide whether equal versions are reinstallable (useful for repair) or rejected.
- Pre-release tags (`-rc1`) shouldn't be accepted by production update logic unless the device is
  in a beta channel.
- Downgrades: allowed only above the security counter floor, and only if data migrations are
  reversible (settings format version).

## Compatibility identifiers
Embed and check before accepting an image:
- **Hardware/board ID and revision range** (`hw_id = 0x0103`, min/max rev): prevents flashing a
  Rev B image onto Rev A boards with a different pinout.
- **Product/variant ID**: different SKUs sharing an MCU.
- **Bootloader interface version**: app requires bootloader >= N.
- **Data/settings schema version**: app migrates forward; refuse downgrade across incompatible
  schema changes.
Put these in the header or manifest that is covered by the signature.

## Where versions come from
Generate them in CI from git tags (`v2.4.1`) plus the CI build number; never type them by hand.
`imgtool sign --version 2.4.1+${CI_BUILD}`.

## Verify
- [ ] Update logic unit tests: newer, equal, older, older-but-above-security-floor, wrong hardware ID.
- [ ] A Rev A board refuses a Rev B-only image.

## Checked
2026-10-31. Confirmed against the MCUboot design page (`ih_ver` with revision and build number), the imgtool page (`--version`, `--security-counter`), the ESP-IDF OTA page (`secure_version` in `esp_app_desc_t`, eFuse comparison) and semver.org (numeric comparison of major/minor/patch, pre-release identifiers). The hardware ID value, version strings and CI example are illustrative placeholders. Removed the claim that `esp_app_desc_t.version` is a string field, which the fetched page does not state.
Method: documentation only; no commands were run.

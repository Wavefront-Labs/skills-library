---
id: computing-software.firmware-embedded-development.esp-idf.app-descriptor-and-version-checks
name: app-descriptor-and-version-checks
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ota, esp-app-desc, app-version, project-ver, ota-version-check, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use the ESP-IDF app descriptor (esp_app_desc_t) for firmware version, build info and secure version, and compare it during OTA to reject downgrades or wrong images."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/misc_system_api.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/ota.rst
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/system/app_image_format.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_app_format/Kconfig.projbuild
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App descriptor and version checks

Every IDF app image carries an `esp_app_desc_t` at a fixed offset: project name, version,
IDF version, build date/time, secure version and ELF SHA256.

## Set the version
Priority: `CONFIG_APP_PROJECT_VER` if `CONFIG_APP_PROJECT_VER_FROM_CONFIG` is set; otherwise `PROJECT_VER` set in the top-level CMakeLists (before `project.cmake` is included), then a `version.txt` file in the project directory, then `git describe`; if none is available the version is "1".
```cmake
set(PROJECT_VER "1.4.2")
project(sensor)
```
Use semantic versions; `git describe` strings like `v1.4.2-3-gabc123-dirty` are hard to compare.

## Read at runtime
```c
#include "esp_app_desc.h"
const esp_app_desc_t *d = esp_app_get_description();
ESP_LOGI(TAG, "%s %s (IDF %s, %s %s)", d->project_name, d->version, d->idf_ver, d->date, d->time);
char sha[17]; esp_app_get_elf_sha256(sha, sizeof sha);
```

## Check an incoming OTA image before writing it
With `esp_https_ota_begin`:
```c
esp_app_desc_t new_desc;
ESP_ERROR_CHECK(esp_https_ota_get_img_desc(handle, &new_desc));
if (strcmp(new_desc.project_name, d->project_name) != 0) return ESP_ERR_INVALID_ARG;  /* wrong product */
if (semver_cmp(new_desc.version, d->version) <= 0) return ESP_ERR_INVALID_VERSION;   /* same or older */
```
With `esp_ota_ops`, the descriptor is at offset `sizeof(esp_image_header_t) + sizeof(esp_image_segment_header_t)`
of the image: buffer the first bytes, then parse.

## Reproducible info
`CONFIG_APP_REPRODUCIBLE_BUILD` removes build date and time from the app descriptor so identical sources give identical binaries. `CONFIG_APP_COMPILE_TIME_DATE` (only offered when reproducible builds are off) controls whether date and time are stored, and `CONFIG_APP_PROJECT_VER_FROM_CONFIG` takes the version from Kconfig.

## Version checks are not security
A string check stops accidental downgrades. Against an attacker serving old signed firmware,
use secure version anti-rollback (eFuse-backed) together with Secure Boot.

## Verify
- [ ] Device reports the exact version in logs and telemetry.
- [ ] OTA of an older or other-product image is rejected before the partition is erased.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed: version source priority, descriptor offset (image header + segment header), esp_app_get_description, esp_app_get_elf_sha256 and esp_https_ota_get_img_desc signatures (headers), secure version via CONFIG_BOOTLOADER_APP_SECURE_VERSION, reproducible-build options. Wrong: CONFIG_APP_EXCLUDE_PROJECT_VER_VAR was described as a reproducible-build switch (it is not; use CONFIG_APP_REPRODUCIBLE_BUILD); version priority omitted the Kconfig override.
Method: documentation only; no commands were run.

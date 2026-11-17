---
id: computing-software.firmware-embedded-development.zephyr.west-binary-blobs
name: west-binary-blobs
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [west-blobs, module-yml-blobs, binary-blobs, west-blobs-fetch, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Handle binary blobs in Zephyr modules: declare them in module.yml, fetch with west blobs, verify checksums, and gate builds that need them via Kconfig."
sources:
  - https://docs.zephyrproject.org/latest/contribute/bin_blobs.html
  - https://docs.zephyrproject.org/latest/develop/west/zephyr-cmds.html#working-with-binary-blobs-west-blobs
  - https://docs.zephyrproject.org/latest/develop/modules.html#module-yaml-file-description
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/drivers/counter/Kconfig.silabs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary blobs

Zephyr policy: no binary blobs in git repositories. Vendor firmware (Wi-Fi/BT controller
images, RF calibration, closed libraries) is declared in the owning module's `module.yml` and
downloaded on demand.

## Fetch
```bash
west blobs list                     # metadata of all declared blobs
west blobs fetch hal_espressif      # download for one module (or omit for all)
west blobs clean hal_espressif
```
Blobs land in `<module>/zephyr/blobs/<path>`. The `sha256` in `module.yml` is checked by
`west blobs` after download (needed for reproducibility). Useful options: `west blobs list -f
'{module}: {type} {path}'`, `west blobs fetch <module> --allow-regex '<regex>'`, and the
`blobs.auto-cache`, `blobs.cache-dirs` and `blobs.mirrors` config options for caches and mirrors.

## Declaring blobs in your own module
`zephyr/module.yml`:
```yaml
name: acme-radio
build:
  cmake: .
  kconfig: Kconfig
blobs:
  - path: fw/radio_fw_v3.bin
    sha256: 2a9b...e1
    type: img                # img or lib
    version: '3.2.1'
    license-path: zephyr/blobs/LICENSE.radio
    url: https://downloads.acme.example/radio_fw_v3.bin
    description: "Radio coprocessor firmware"
    doc-url: https://acme.example/radio
```
`path` is relative to the module's `zephyr/blobs/` folder and `license-path` to the module root.
`url` may be a list (each entry is a fallback). Optional keys: `click-through`, `size`, `fetcher`.

## Using blobs in the build
- Reference them through `${ZEPHYR_<MODULE>_MODULE_DIR}/zephyr/blobs/...` in CMake.
- Zephyr generates `ZEPHYR_<MODULE>_MODULE_BLOBS` for modules that declare blobs; make blob-
  dependent Kconfig symbols `depends on` it.
- Blob types are `img` (firmware image) and `lib` (precompiled library); a miscellaneous
  binary data file is also an allowed kind of blob in the policy.
- Print a clear CMake error if a needed file is missing:
```cmake
if(NOT EXISTS ${blob})
  message(FATAL_ERROR "Missing blob: run 'west blobs fetch acme-radio'")
endif()
```
- Tainting: an image that includes blobs is tainted. One or more `TAINT_BLOBS_*` Kconfig options
  are set to `y`, the configuration phase warns (can be disabled in Kconfig), `west spdx`
  reports it, and the fatal error handler and boot banner print the tainted status.

## CI
Add `west blobs fetch <modules>` after `west update`; point `blobs.auto-cache` or `blobs.cache-dirs`
at a CI-cached directory to avoid re-downloading (cached files are looked up by filename, optionally
with a SHA-256 suffix).

## Verify
- [ ] `west blobs fetch` succeeds in CI and the files exist under each module's `zephyr/blobs/`.
- [ ] Builds without the blob fail with a message naming the fetch command.
- [ ] Licence files for each blob are shipped with release artefacts as required.

## Checked

2026-10-26. Zephyr docs main branch (latest release v4.4.2). Confirmed the blobs: keys in module.yml and their relative-path rules (modules page), west blobs list/fetch/clean, --allow-regex and cache/mirror options (west zephyr-cmds page), SHA-256 check after download, allowed types and tainting behaviour (contribute/bin_blobs page). Wrong in the draft: BUILD_ONLY_NO_BLOBS does not make blob code fail early (it is used by build-only builds such as twister so blob-dependent code builds without blobs, per Kconfig help text); removed the unconfirmed git-ignore and refuse-mismatch claims.
Method: documentation only; no commands were run.

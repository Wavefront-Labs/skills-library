---
id: computing-software.firmware-embedded-development.esp-idf.esp-idf-docker-builds
name: esp-idf-docker-builds
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-build, esp-idf-docker, espressif-idf-image, ci-builds, reproducible-build, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Build ESP-IDF projects reproducibly in the official espressif/idf Docker image for CI and teams, with pinned versions, caching and flashing from the host."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/tools/idf-docker-image.rst
  - https://hub.docker.com/r/espressif/idf
  - https://github.com/espressif/esp-idf-ci-action/blob/master/README.md
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-guides/tools/idf-component-manager.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESP-IDF Docker builds

## Build a project
```bash
docker run --rm -v "$PWD":/project -w /project -u $UID \
  -e HOME=/tmp espressif/idf:v5.3 idf.py set-target esp32s3 build
```
- Pin a release tag (`vX.Y` tracks a release; `release-vX.Y` tracks the release branch; `latest` tracks `master`); avoid `latest` for reproducible builds.
- `-u $UID` makes files be created as you, and `HOME=/tmp` gives the user a home for the `~/.cache` files `idf.py` creates.
- The image entrypoint sets `PATH` and activates the Python virtual environment, so `idf.py` is ready to use.

## Interactive shell
```bash
docker run --rm -it -v "$PWD":/project -w /project -u $UID -e HOME=/tmp espressif/idf:v5.3
```

## Component manager cache
Managed components download on every clean build unless you persist the component manager's cache between runs (see the component manager documentation for the cache location). Commit `dependencies.lock` (the component manager writes it at the project root with the full dependency list) so CI resolves the same versions.

## GitHub Actions
```yaml
- uses: espressif/esp-idf-ci-action@v1
  with:
    esp_idf_version: v5.3
    target: esp32s3
    path: firmware
```

## Flashing
`idf.py flash` and `idf.py monitor` do not work in the container unless the serial port is passed through. On Linux add the device with `--device` or `--privileged` (and make sure the `-u` user can read and write it), or use esptool's remote serial ports (`rfc2217://`) from the container. Otherwise build in Docker and flash from the host:
```bash
pip install esptool
cd build && esptool --chip esp32s3 -b 460800 write-flash @flash_args
```

## Custom images
Extend the official image for extra tools rather than installing IDF yourself:
```dockerfile
FROM espressif/idf:v5.3
RUN pip install --no-cache-dir <extra-python-package>
```

## Pitfalls
- Git "dubious ownership" errors when the mounted repository is owned by a different user: designate the directory as safe by setting `IDF_GIT_SAFE_DIR` when starting the container (see the image guide for the exact form), or run with a matching uid.

## Verify
- [ ] Two clean builds from the same commit produce identical app `.bin` checksums (with
  `CONFIG_APP_REPRODUCIBLE_BUILD=y`).
- [ ] CI uses the same image tag as developers (documented in the README).

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the IDF Docker image guide and esp-idf-ci-action README: image name and tag scheme (latest, vX.Y, release-vX.Y), docker run options (-v, -w, -u, HOME), entrypoint environment, serial passthrough limits and rfc2217, IDF_GIT_SAFE_DIR for dubious ownership, esp-idf-ci-action@v1 inputs (esp_idf_version, target, path), dependencies.lock, CONFIG_APP_REPRODUCIBLE_BUILD, esptool v5 write-flash naming. Wrong: patch tags such as v5.3.1 are not in the documented tag scheme (vX.Y); IDF_COMPONENT_CACHE_PATH and the cache mount path were unconfirmed and removed, as were the Windows bind-mount speed, .idf-version and pytest-embedded claims.
Method: documentation only; no commands were run.

---
id: computing-software.firmware-embedded-development.platformio.firmware-release-artifacts
name: firmware-release-artifacts
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [firmware-release-artifacts, github-release, release-workflow, checksums, elf-archive, merged-image, platformio-ci, platformio, firmware-embedded-development]
level: practitioner
status: draft
description: "Publish firmware releases from PlatformIO CI: build per env on tags, collect bin/hex/elf/map, name with version, checksums and manifest, attach to a GitHub Release, keep ELFs."
sources:
  - https://docs.platformio.org/en/latest/integration/ci/github-actions.html
  - https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts
  - https://cli.github.com/manual/gh_release_create
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Release artefacts

## What to ship per environment
- Flashable image(s): `.bin` / `.hex` / `.uf2`; for ESP32 a merged factory image plus the OTA app
  binary; for MCUboot a signed image.
- `.elf` and `.map` (symbols for crash decoding and size analysis) — archive even if not public.
- `SHA256SUMS`, and a small `manifest.json` (version, git sha, env, board, file names, sizes,
  platform/package versions from `pio pkg list`).

## Workflow (GitHub Actions)
```yaml
name: release
on:
  push:
    tags: ["v*"]
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix: { env: [esp32s3, nucleo_g474re] }
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }                 # tags for git describe
      - uses: actions/cache@v4
        with:
          path: |
            ~/.platformio
            .pio/libdeps
          key: pio-${{ matrix.env }}-${{ hashFiles('platformio.ini') }}
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install platformio
      - run: FW_VERSION=${GITHUB_REF_NAME#v} pio run -e ${{ matrix.env }}
      - name: Collect
        run: |
          V=${GITHUB_REF_NAME#v}; E=${{ matrix.env }}; D=dist/$E; mkdir -p $D
          for f in .pio/build/$E/firmware.{bin,hex,elf,map}; do
            [ -f "$f" ] && cp "$f" "$D/fw-$V-$E.${f##*.}"
          done
          (cd $D && sha256sum * > SHA256SUMS)
      - uses: actions/upload-artifact@v4
        with: { name: fw-${{ matrix.env }}, path: dist/${{ matrix.env }} }
  publish:
    needs: build
    runs-on: ubuntu-latest
    permissions: { contents: write }
    steps:
      - uses: actions/download-artifact@v4
        with: { path: dist }
      - run: gh release create "$GITHUB_REF_NAME" dist/*/* --repo "$GITHUB_REPOSITORY" --generate-notes
        env: { GH_TOKEN: "${{ github.token }}" }
```
Attach `.elf` files to an internal store instead of the public release if symbols are sensitive.

## Practices
- Build releases only from tags, in CI, never from developer machines.
- Version embedded in the binary must equal the tag (see generated version header).
- Pin platform and library versions on release branches; record `pio pkg list` output in the
  manifest for reproducibility.
- Sign images in CI with keys from a secret store/HSM; never commit private keys.

## Verify
- [ ] Release contains every env's artefacts with matching checksums.
- [ ] A downloaded artefact flashes and reports the tag version.

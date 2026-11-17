---
id: computing-software.firmware-embedded-development.arduino.board-manager-package-index
name: board-manager-package-index
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [package-index, package-json, boards-manager-url, platform-release, tools-dependencies, checksum, arduino, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Publish an Arduino core through Boards Manager: package_<name>_index.json structure, platform and tool entries, checksums and sizes, host triplets, and versioned releases."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/package_index_json-specification.md
  - https://github.com/arduino/arduino-cli/blob/master/docs/platform-specification.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Boards Manager package index

Users add your URL under "Additional boards manager URLs"; the IDE/CLI downloads the JSON and offers
every platform version listed in it.

## Structure
```json
{
  "packages": [{
    "name": "acme",
    "maintainer": "Acme",
    "websiteURL": "https://acme.example",
    "email": "dev@acme.example",
    "help": { "online": "https://acme.example/support" },
    "platforms": [{
      "name": "Acme SAMD Boards",
      "architecture": "samd",
      "version": "1.2.0",
      "category": "Contributed",
      "url": "https://github.com/acme/acme-core/releases/download/1.2.0/acme-samd-1.2.0.tar.bz2",
      "archiveFileName": "acme-samd-1.2.0.tar.bz2",
      "checksum": "SHA-256:3b1f...",
      "size": "1458321",
      "boards": [{ "name": "Acme Sense" }],
      "toolsDependencies": [
        { "packager": "arduino", "name": "<tool name>", "version": "<tool version>" }
      ]
    }],
    "tools": []
  }]
}
```
- The FQBN becomes `acme:samd:<board id from boards.txt>`.
- `toolsDependencies` may reference other packagers' tools (Arduino's compilers) so you do not
  host toolchains. Own tools go in `tools[]` with one `systems[]` entry per host:
  `x86_64-linux-gnu`, `arm-linux-gnueabihf`, `aarch64-linux-gnu`, `i686-mingw32`, `x86_64-mingw32`,
  `arm64-mingw32`, `i686-apple-darwin`, `x86_64-apple-darwin`, `arm64-apple-darwin`, each with `url`,
  `archiveFileName`, `checksum` and `size` (the table in the specification is authoritative).
- `checksum` and `size` must match the archive byte-for-byte; mismatch = install failure.
- The archive must contain a single folder in its root (other root files and `__MACOSX` are ignored),
  holding the platform files (`platform.txt`, `boards.txt`, `cores/`, `variants/`, ...) with the architecture
  folder level (such as `avr`) removed.

## Release workflow
1. Tag the core repo; CI builds the archive (one root folder), computes its SHA-256 checksum and size in bytes.
2. Append a new platform entry to the index (keep old versions so users can downgrade).
3. Publish the JSON at a stable URL (GitHub Pages, release asset with fixed name).
4. Test: `arduino-cli core update-index --additional-urls <url>` and
   `arduino-cli core install acme:samd@1.2.0`.

## Gotchas
- Editing an already-published archive without changing the version breaks checksums for users;
  always release a new version.
- `"category"` must be `Contributed` for third-party platforms.
- Use `"discoveryDependencies"` / `"monitorDependencies"` for pluggable discovery/monitor tools.

## Verify
- [ ] Clean install via CLI on Linux, macOS and Windows succeeds.
- [ ] `arduino-cli board listall acme` lists every board.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 docs on master (commit 2026-10-22).

Confirmed: package fields (`name`, `maintainer`, `websiteURL`, `email`, `help.online`), platform fields (`archiveFileName`, `checksum` as `ALGORITHM:CHECKSUM` with MD5, SHA-1 or SHA-256 supported and SHA-256 recommended, `size` in bytes, `category`, `toolsDependencies`, `discoveryDependencies`, `monitorDependencies`); tools use a `systems` array whose entries carry `host`, `url`, `archiveFileName`, `checksum`, `size`; archive must contain a single folder in its root and the architecture folder level is removed; third-party platforms must set `category` to `Contributed`. Fixed: the host list now follows the specification table (Windows Arm64 added); the tool versions in the example are placeholders because the documented examples use different ones. Removed the unconfirmed remarks about slow large indexes and `sha256sum`.

Method: documentation only; no commands were run.

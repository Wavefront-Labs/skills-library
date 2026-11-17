---
id: computing-software.firmware-embedded-development.platformio.publishing-packages-to-registry
name: publishing-packages-to-registry
category: computing-software
field: firmware-embedded-development
product: platformio
tags: [pio-pkg-publish, pio-pkg-pack, platformio-registry, library-json, package-versioning, platformio, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Publish libraries, tools or platforms to the PlatformIO Registry with pio pkg pack/publish: library.json essentials, owners and private packages, versioning and unpublishing."
sources:
  - https://docs.platformio.org/en/latest/core/userguide/pkg/cmd_publish.html
  - https://docs.platformio.org/en/latest/manifests/library-json/index.html
  - https://docs.platformio.org/en/latest/core/userguide/pkg/cmd_pack.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing packages to the PlatformIO Registry

## Manifest (library.json)
```json
{
  "name": "AcmeSensor",
  "version": "1.4.0",
  "description": "Driver for the ACME TMP42 temperature sensor (I2C)",
  "keywords": ["sensor", "temperature", "i2c"],
  "repository": { "type": "git", "url": "https://github.com/acme/AcmeSensor.git" },
  "authors": [{ "name": "ACME Firmware", "email": "fw@acme.example", "maintainer": true }],
  "license": "MIT",
  "frameworks": ["arduino", "espidf"],
  "platforms": "*",
  "headers": "AcmeSensor.h",
  "export": { "exclude": ["extras/*", "test/*", ".github/*"] },
  "dependencies": [{ "owner": "bblanchon", "name": "ArduinoJson", "version": "^7.0.0" }]
}
```
`name` + `version` (semver) identify the release. `frameworks`/`platforms` drive
compatibility filtering in LDF. Arduino-style `library.properties` is also accepted, but
`library.json` controls more.

## Pack and inspect
```bash
pio pkg pack                       # creates AcmeSensor-1.4.0.tar.gz honoring export rules
tar tzf AcmeSensor-1.4.0.tar.gz    # check nothing secret or huge slipped in
```

## Publish
```bash
pio account login                  # or PLATFORMIO_AUTH_TOKEN in CI
pio pkg publish                    # from the package dir (or pass the tarball)
pio pkg publish --owner acme       # publish under an organization
pio pkg publish --private          # visible only to the owner/org
pio pkg publish --type tool        # --type sets a custom package type (see pio pkg install types)
```
Users then depend on it as `lib_deps = acme/AcmeSensor@^1.4.0`.

## Versioning rules
- A published version is immutable, and a name+version pair can never be reused even after it is
  unpublished: fix mistakes with a new version.
- `pio pkg unpublish acme/AcmeSensor@1.4.0` removes one version, and only within 72 hours of the
  publish date (use sparingly: builds pinning it break). Without `@version` it removes the whole
  package. `--undo` puts a removed version back.
- Private packages depend on the registry plan; check the Registry pricing page.
- Follow semver honestly: users pin with `^`, so breaking changes need a major bump.

## Automate on tags
```yaml
# GitHub Actions excerpt
on: { push: { tags: ['v*'] } }
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install platformio
      - run: pio pkg publish --no-interactive
        env: { PLATFORMIO_AUTH_TOKEN: "${{ secrets.PIO_TOKEN }}" }
```
(`pio account token` creates the token.) Check that the tag matches `version` in
`library.json` before publishing (a one-line script step).

## Verify
- [ ] `pio pkg pack` archive contains only intended files.
- [ ] A clean project with `lib_deps = acme/AcmeSensor@^1.4.0` resolves and builds for each listed framework.
- [ ] Tag-to-version consistency checked in CI.

## Checked
2026-11-01. Confirmed in the platformio-docs repo: `pio pkg publish` options (`--owner`, `--type`, `--private`,
`--no-interactive`), name+version never reusable, `pio pkg pack` tarball, `pio pkg unpublish` (72-hour window,
`--undo`, whole package without a version), `pio account token` and `PLATFORMIO_AUTH_TOKEN`, library.json `frameworks`
and `dependencies` (owner/name/version). Removed: the unconfirmed claim that the registry runs extra checks and the
library auto-detection claim.
Method: documentation only; no commands were run.

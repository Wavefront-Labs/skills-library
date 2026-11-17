---
id: computing-software.firmware-embedded-development.arduino.sketch-yaml-build-profiles
name: sketch-yaml-build-profiles
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-cli, sketch-profiles, sketch-yaml, reproducible-builds, dump-profile, default-fqbn, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Pin Arduino cores and libraries per sketch with sketch.yaml build profiles: profile syntax, third-party platform URLs, generating profiles with --dump-profile, and using them in CI."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/sketch-project-file.md
  - https://github.com/arduino/arduino-cli/blob/master/internal/cli/compile/compile.go
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sketch.yaml build profiles

By default `arduino-cli` builds with whatever cores and libraries are installed globally, so two
machines can produce different binaries from the same sketch. A **profile** in `sketch.yaml`
(next to the `.ino`) pins the exact platform and library versions; arduino-cli installs them in
an isolated location for that build.

## Example
```yaml
# MySketch/sketch.yaml
profiles:
  uno:
    notes: Production build for the Uno R3 controller board
    fqbn: arduino:avr:uno
    platforms:
      - platform: arduino:avr (1.8.4)
    libraries:
      - ArduinoIoTCloud (1.0.2)
      - dependency: Arduino_ConnectionHandler (0.6.4)
      - dir: ../MyLocalLib             # path relative to the sketch folder (CLI 1.3.0+)

  tiny:
    fqbn: attiny:avr:ATtinyX5:cpu=attiny85,clock=internal16
    platforms:
      - platform: attiny:avr (1.0.2)
        platform_index_url: https://raw.githubusercontent.com/damellis/attiny/ide-1.6.x-boards-manager/package_damellis_attiny_index.json
      - platform: arduino:avr (1.8.3)
    libraries:
      - TinyDHT sensor library (1.1.0)

default_profile: uno
```
- Profile builds exclude globally installed platforms and libraries, so list every library the
  sketch needs; mark transitive ones with `dependency:`.
- Board options (menu settings) go into the FQBN after `:`.
- Third-party cores need `platform_index_url` on the platform entry (optional for official `arduino:*` platforms).
- A platform dependency of the target platform is listed as a second `platforms` entry (as `arduino:avr` above).

## Use
```bash
arduino-cli compile --profile tiny MySketch
arduino-cli compile MySketch                 # uses default_profile
arduino-cli upload  --profile uno -p <port> MySketch
```

## Generate a profile from a working setup
```bash
arduino-cli compile --fqbn arduino:avr:uno --dump-profile MySketch
```
prints a profile with the exact platform and library versions used by that build. Paste it
into `sketch.yaml` and you've frozen the current working state.

## Profiles vs other defaults
`sketch.yaml` can also hold `default_fqbn`, `default_programmer`, `default_port`,
`default_port_config`, `default_protocol` and `default_profile` as defaults for the matching flags;
only a profile build is isolated from globally installed platforms and libraries.

## Upgrading
Change one version at a time on a branch, rebuild all profiles and run the hardware smoke test.
Library major-version bumps can change APIs.

## Verify
- [ ] Clean machine (or fresh CI runner): `arduino-cli compile --profile <p>` succeeds with only `arduino-cli` installed.
- [ ] Every `#include`d library appears in the profile.
- [ ] Release tags build the same binary twice (compare hashes).

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 docs and source on master (commit 2026-10-22).

Confirmed: profile grammar (`notes`, `fqbn`, `programmer`, `platforms` with `platform: name (version)` and `platform_index_url`, `libraries` with `dependency:` and `dir:`, `port`, `port_config`, `protocol`); `dir:` since 1.3.0 and port fields since 1.1.0; profile builds exclude globally installed platforms and libraries; `default_profile` triggers a profile build; `default_fqbn`, `default_programmer`, `default_port`, `default_port_config`, `default_protocol`; `compile --profile` (also `-m`) and `--dump-profile`. Removed unconfirmed claims: the JSON size output, pinned example versions not in the docs, the ESP32 option names.

Method: documentation only; no commands were run.

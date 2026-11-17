---
id: computing-software.firmware-embedded-development.arduino.library-properties-depends
name: library-properties-depends
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [library-depends, library-properties, depends-field, version-constraint, includes-field, dependency-resolution, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Declare Arduino library dependencies in library.properties: depends= syntax with version constraints, includes=, how IDE/CLI install them, and avoiding dependency conflicts."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/library-specification.md
  - https://github.com/arduino/arduino-lint/blob/main/internal/rule/ruleconfiguration/ruleconfiguration.go
  - https://github.com/bblanchon/ArduinoJson/blob/master/src/ArduinoJson/version.hpp
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Library dependencies (library.properties depends)

## Declaring
```properties
name=Acme Sensor
version=1.3.0
author=Acme <dev@acme.example>
maintainer=Acme <dev@acme.example>
sentence=Driver for the Acme sensor.
paragraph=I2C driver with low-power modes.
category=Sensors
url=https://github.com/acme/AcmeSensor
architectures=*
depends=Adafruit BusIO (>=1.14.0), ArduinoJson (>=7.0.0 && <8.0.0)
includes=AcmeSensor.h
```
- `depends` (IDE 1.8.10 / CLI 0.7.0 and later) is a comma-separated list of library names; names may contain
  spaces. Arduino Lint requires them to be in the Library Manager index and treats them as case-sensitive.
- Version constraints in parentheses (CLI 0.7.0 / IDE 2.0.0-beta.3 and later): operators `=`, `>`, `>=`, `<`, `<=`,
  combined with `&&`, `||` and parentheses, for example `(>=1.0.0 && <2.0.0)`; `!` needs CLI 0.22.0.
  No constraint installs the latest version.
- `includes=` lists the headers the IDE's "Include library" command adds to a sketch (all root-folder
  headers when it is missing).

## How tools use it
- IDE Library Manager and `arduino-cli lib install X` offer to install dependencies too
  (`--no-deps` to skip). `arduino-cli lib deps X` prints the resolved tree and what is missing.
- Dependencies are resolved at install time only. The build itself does not read `depends`; it
  just resolves `#include`s against installed libraries.

## Good practice
- Depend only on libraries in the Library Manager registry; a dependency that is not indexed
  makes installation fail for users.
- Use lower bounds for features you need and upper bounds for majors you have not tested.
- Avoid depending on a library just for one small helper; copy it with its licence or make it
  optional with `__has_include(<X.h>)`.
- Don't vendor a dependency inside your library folder under the same header name; two libraries then
  match the same `#include` and the build picks one by the resolution rules.

## Gotchas
- A dependency name that is not in the Library Manager index is flagged by `arduino-lint` (rule LP048).
- Constraints are honoured only at install; a user upgrading the dependency later can break you.
  Check versions at compile time if critical:
  ```cpp
  #if ARDUINOJSON_VERSION_MAJOR != 7
  #error "AcmeSensor needs ArduinoJson 7"
  #endif
  ```

## Verify
- [ ] `arduino-cli lib install "Acme Sensor"` on a clean setup installs all deps and examples
  compile.
- [ ] `arduino-lint --library-manager update` passes.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 library specification on master (commit 2026-10-22); Arduino Lint rule definitions (latest commit 2026-10-18); ArduinoJson 7.4.2 source.

Confirmed: `depends` is comma separated, available from IDE 1.8.10 and CLI 0.7.0, and `lib install` installs dependencies; version constraints use `=`, `>`, `>=`, `<`, `<=`, `&&`, `||`, parentheses, with `!` from CLI 0.22.0; no constraint installs the latest version; `includes` feeds the Include library command (all root headers when missing); lint rule LP048 flags `depends` names not in the Library Manager index and says names are case-sensitive; `ARDUINOJSON_VERSION_MAJOR` exists. Fixed: version constraints were attributed to IDE 1.8.10 but the specification says IDE 2.0.0-beta.3 and CLI 0.7.0. Removed: the older-IDE typo remark and the quoted "Multiple libraries" message.

Method: documentation only; no commands were run.

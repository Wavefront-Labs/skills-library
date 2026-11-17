---
id: computing-software.firmware-embedded-development.arduino.library-keywords-and-examples
name: library-keywords-and-examples
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-library, keywords-txt, library-examples, src-layout, library-specification, syntax-highlighting, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Lay out an Arduino library per the 1.5 library specification: src/ layout, examples/ sketches that compile in CI, and a correctly tab-separated keywords.txt."
sources:
  - https://github.com/arduino/arduino-cli/blob/master/docs/library-specification.md
  - https://github.com/arduino/arduino-lint/blob/main/internal/rule/ruleconfiguration/ruleconfiguration.go
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arduino library layout, keywords and examples

**Goal:** a library that installs cleanly, shows its examples in File > Examples, gets
syntax highlighting, and passes `arduino-lint`.

## Layout (1.5 format)
```
MySensor/
  library.properties
  keywords.txt
  README.md, LICENSE
  src/
    MySensor.h          # the header users #include
    MySensor.cpp
    internal/regs.h     # subfolders allowed in src/ (compiled recursively)
  examples/
    BasicRead/BasicRead.ino      # folder name == sketch name
    LowPower/LowPower.ino
  extras/               # docs, images; never compiled
```
The legacy layout (sources in the root plus a `utility/` folder) does not compile nested source folders;
code in nested folders must be in `src/`. The folder must be named exactly `examples`.

## keywords.txt
Fields are separated by a single true tab (not spaces): `KEYWORD<TAB>KEYWORD_TOKENTYPE`, with optional
`REFERENCE_LINK` and `RSYNTAXTEXTAREA_TOKENTYPE` fields after it.
```
MySensor	KEYWORD1
begin	KEYWORD2
readTemperature	KEYWORD2
MYSENSOR_ADDR_DEFAULT	LITERAL1
```
`KEYWORD1` = datatypes, `KEYWORD2` = functions, `KEYWORD3` = structures, `LITERAL1` = constants.
The IDE colors a keyword of any installed library when it appears in a sketch.

## Examples
- Each example is a full sketch that compiles on every architecture the library claims.
- Start with the simplest working use (`begin()`, one read, print) and keep hardware
  assumptions visible (pins, I2C address) as constants at the top.

## CI
```yaml
- uses: arduino/arduino-lint-action@v1
  with: { library-manager: update, compliance: strict }
- uses: arduino/compile-sketches@v1
  with:
    fqbn: arduino:avr:uno
    libraries: |
      - source-path: ./
    sketch-paths: |
      - examples
```
Add a matrix of FQBNs matching `architectures=`.

## Verify
- [ ] `arduino-lint --compliance strict` passes.
- [ ] All examples compile for every FQBN in the matrix.
- [ ] Examples appear in the IDE's Examples menu after installing the library.

## Checked

Date: 2026-10-25. Documentation release: Arduino CLI 1.5.1 library specification on master (commit 2026-10-22); Arduino Lint rule definitions (commit 2026-10-18).

Confirmed: 1.5 layout with `src/` compiled recursively, legacy root and `utility/` layout not recursive; `examples` folder name exact lower case, sketches shown in the Examples menu; `extras` ignored by the software; keywords.txt in the library root, fields separated by a single true tab, token types KEYWORD1, KEYWORD2, KEYWORD3, LITERAL1, LITERAL2 and the optional REFERENCE_LINK and RSYNTAXTEXTAREA_TOKENTYPE fields; arduino-lint has example-folder rules (stray sketch, missing examples, folder name case); arduino-lint-action `library-manager` and `compliance` inputs; compile-sketches `libraries` and `sketch-paths` inputs. Removed claims that are not documented: how IDE 2.x uses keywords.txt, that arduino-lint checks keywords.txt (no keywords rule exists in the rule list), and the `while (!Serial)` example hang.

Method: documentation only; no commands were run.

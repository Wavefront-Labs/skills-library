---
id: computing-software.software-engineering.crystal.yaml-serializable
name: yaml-serializable
category: computing-software
field: software-engineering
product: crystal
tags: [yaml-serializable, json-yaml, yaml, yaml-parse, yaml-any, to-yaml, config-file, yaml-field, anchors, crystal]
level: practitioner
status: docs-checked
description: "Parse YAML with YAML.parse and YAML::Any, map to types with YAML::Serializable, and generate YAML safely with to_yaml."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# YAML parsing and YAML::Serializable

Goal: read config files.

- `require "yaml"` (needs libyaml).
- Dynamic: `y = YAML.parse(File.read("c.yml"))`, `y["db"]["port"].as_i`, `as_s`, `as_a`, `as_h`.
- Typed: `class Config; include YAML::Serializable; property host : String; property port : Int32 = 5432; end`, then `Config.from_yaml(str)`.
- Field options mirror JSON: `@[YAML::Field(key: "x", ignore: true, converter: ...)]`; `YAML::Serializable::Strict` and `Unmapped` exist as in JSON.
- Output: `obj.to_yaml`, `YAML.build { |y| y.mapping { ... } }`.
- Anchors and aliases (`&a`, `*a`) are resolved by the parser; `<<` merge keys supported.

Gotchas:
- YAML implicit typing: `no`, `1.0`, dates may parse as non-strings; quote them in the file.
- Errors: `YAML::ParseException`.
- Never parse untrusted YAML into huge structures without size limits.

Verify: spec loading a config string with defaults.

## Checked

Date 2026-11-03. Confirmed YAML.parse and YAML::Any, the YAML::Field options (key, ignore, converter, presence, emit_null), YAML::Serializable::Strict and Unmapped, YAML.build, to_yaml, merge key (<<) resolution in the core schema, YAML::ParseException, and the libyaml link (Link yaml) in the YAML source. Removed the duplicated error entry.

Method: documentation only; no commands were run.

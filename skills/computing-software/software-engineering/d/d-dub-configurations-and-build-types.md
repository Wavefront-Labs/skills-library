---
id: computing-software.software-engineering.d.d-dub-configurations-and-build-types
name: d-dub-configurations-and-build-types
category: computing-software
field: software-engineering
product: d
tags: [d-dub-configurations-and-build-types, dub-configuration, buildtypes, subconfiguration, build-type, release, debug, unittest-cov, plain, profile, ddox, custom-buildtype, d]
level: practitioner
status: docs-checked
description: "Create multiple configurations (app, unittest, lib), set subConfiguration for dependencies, define custom buildTypes, and use the built-in debug/release/unittest/cov types."
sources:
  - https://dub.pm/dub-reference/configurations/
  - https://dub.pm/dub-reference/buildtypes/
  - https://dub.pm/dub-reference/build_settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DUB configurations, subConfigurations and build types

Goal: build variants from one recipe.

```
configuration "app" { targetType "executable" }
configuration "unittest" { targetType "executable" ; mainSourceFile "tests/main.d" ; dependency "silly" version="~>1.1" }
subConfiguration "vibe-d" "libasync"
buildType "ci" {
    buildOptions "releaseMode" "optimize" "inline"
    dflags "-preview=dip1000"
}
```
- Built-in types (defined mostly via `buildOptions`): `debug` (`debugMode`, `debugInfo`), `plain`, `release` (`releaseMode`, `optimize`, `inline`), `release-debug`, `release-nobounds`, `unittest`, `unittest-cov`, `docs`, `ddox`, `profile`, `profile-gc`, `cov`, `cov-ctfe`, `unittest-cov-ctfe`, `syntax`.
- Select: `dub build -b release`, `dub build -c unittest`, `dub run -b ci`; dub also reads the `DFLAGS` environment variable.
- Per-config and per-buildType settings: `buildType "x" { dflags ... }` is a block in SDL; in JSON `"buildTypes": {"ci": {...}}`.
- Default configuration: with none defined, dub generates `application` (executable) or `library`; with configurations defined, the first one matching the platform is used (`dub build --print-configs` lists them); pick with `-c`.
- Dependencies' configurations: `subConfiguration "dep" "name"`, or `--override-config=<dependency>/<config>` on the command line.

Gotchas:
- `dub test` picks the configuration in this order: `--config`; with `--main-file` the first non-executable one; a configuration named `unittest`; the first non-executable one; the first one.

Verify: `dub build --print-configs` and `dub build --print-builds`.

## Checked

Date 2026-11-02. Confirmed default configuration rules, dub test configuration selection order, built-in build types and subConfiguration (dub reference). Corrected build type contents (including unittest-cov-ctfe) and removed raw dmd flag claims.

Method: documentation only; no commands were run.

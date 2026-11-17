---
id: computing-software.software-engineering.elixir.elixir-otp-version-management
name: elixir-otp-version-management
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, asdf, mise, elixir-install, otp-compatibility, tool-versions, elixir-version-requirement, kiex, version-management, elixir-versions]
level: intro
status: docs-checked
description: "Pair Elixir and Erlang/OTP versions using the official compatibility table, know the support window, and handle deprecations."
sources: ["https://hexdocs.pm/elixir/compatibility-and-deprecations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matching Elixir and Erlang/OTP versions

**Goal:** reproducible toolchain across dev and CI, pairing versions the Elixir project supports.

## Rules
- Elixir uses vMAJOR.MINOR.PATCH. A backwards compatible minor release appears every 6 months; patch releases are unscheduled. Bug fixes go only to the latest minor branch; security patches cover the last 5 minor branches. There are no plans for a major v2.
- Erlang/OTP is versioned independently and releases a new major yearly. Elixir aims to support the last three OTP majors when it is released. Examples from the table (read the live page for current rows): Elixir 1.17 supports OTP 25-27, 1.18 supports 25-27, 1.19 supports 26-28, 1.20 supports 27-29.
- Elixir may add support for a newer OTP in a patch release (for example OTP 26 from Elixir v1.14.5); that release makes only the minimum changes, and the next minor release leverages the new OTP features.
- Pin both the Elixir and OTP versions in every environment (dev, CI, release) from the same compatibility table; test the minimum supported and the latest combination.
- Deprecations take 3 steps: soft-deprecated (changelog and docs only), hard-deprecated (warnings emitted, only after the replacement has existed for at least three minor versions), removed (only on a major release). Fix hard-deprecation warnings; compiling with `--warnings-as-errors` turns new compiler warnings into errors.
- Minor releases can still break code in rare cases: security fixes, bug fixes that code depended on, new compiler warnings, and new auto-imported `Kernel` functions that collide with local ones (resolve with `import Kernel, except: [...]`).
- Experimental features are marked as such and carry no compatibility guarantee.

## Self-check
Print versions with `elixir --version` and compare the OTP major against the compatibility table row for your Elixir minor.

## Checked

Checked 2026-11-09 against the "Compatibility and deprecations" page on hexdocs.pm (Elixir v1.20.5 pages), read in full.
Confirmed: release cadence, support window, the Elixir/OTP compatibility rows quoted, patch-release OTP support, the three-step deprecation policy, and the breaking-change exceptions.
Removed as unconfirmed: asdf and mise `.tool-versions` syntax, the `-otp-NN` suffix, `mix local.hex`/`mix local.rebar`, setup-beam and `hexpm/elixir` Docker images, the `elixir: "~> 1.15"` guidance, and the install page source (not read).

Method: documentation only; no commands were run.

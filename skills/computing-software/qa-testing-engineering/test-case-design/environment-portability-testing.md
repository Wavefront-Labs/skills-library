---
id: computing-software.qa-testing-engineering.test-case-design.environment-portability-testing
name: environment-portability-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [environment-portability, portability-testing, configuration-testing, twelve-factor, adaptability]
level: practitioner
status: docs-checked
description: "Test configuration and environment portability: externalised config, missing or bad settings, OS and locale differences, containers and cloud targets."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta
  - https://12factor.net/config
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration and environment portability testing

**Goal:** the same build artefact runs correctly in every target environment by changing configuration only.

## Checks
- **Same artefact everywhere:** the image or package promoted from test to prod is byte-identical (compare digests); no rebuild per environment.
- **Externalised config** (Twelve-Factor III): grep the codebase for hard-coded hosts, ports, paths, credentials and environment names (`grep -rnE "localhost|prod|\.internal" src/`).
- **Missing config:** remove each required setting; app should fail fast at startup with a clear message naming the setting, not fail at first use hours later.
- **Invalid config:** wrong types, negative timeouts, unreachable URLs; validated at startup.
- **Defaults:** documented and safe (debug off, TLS on).
- **Precedence:** env var vs file vs flag order behaves as documented.
- **Secrets:** read from the secret store or mounted file; never logged at startup (check logs).

## Environment differences
- OS: path separators, case-sensitive filesystems (Linux) vs insensitive (Windows/macOS), line endings, file locking.
- Locale and timezone: run tests with `TZ=Pacific/Auckland LANG=tr_TR.UTF-8` (Turkish dotless i breaks case-insensitive comparisons).
- CPU architecture: amd64 vs arm64 images (native dependencies).
- Container constraints: read-only root filesystem, non-root user, memory limits respected by the runtime (JVM container awareness).
- Cloud differences: storage, queue and DNS behaviours across providers or regions.

## Verify
One artefact passes the smoke suite in each environment with only config changed, and each required setting has a fail-fast test.

## Checked

2026-10-28. Confirmed: Twelve-Factor III Config: config in the environment, strict separation from code, no credentials in the codebase. Removed: Unreadable ISO 25000 source link.

Method: documentation only; no commands were run.

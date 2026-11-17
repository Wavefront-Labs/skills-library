---
id: computing-software.qa-testing-engineering.test-case-design.adaptability-across-environments
name: adaptability-across-environments
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [adaptability-testing, portability-testing, environment-compatibility, container-testing, configuration-testing, istqb-tta]
level: practitioner
status: draft
description: "Test adaptability: the software runs on each supported OS, runtime, database, container platform and configuration without changes beyond documented configuration."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta-v4-0
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Adaptability testing

**Goal:** the product works in every supported environment. CTAL-TTA v4.0 4.6.

## Build the environment matrix
Dimensions: OS and version, CPU architecture (x86_64 vs arm64), language runtime versions (Node 20/22, Python 3.10-3.13, Java 17/21), databases and versions, browsers, container runtimes/Kubernetes versions, cloud providers, locale/time zone.
Use combinatorial selection (`pict-pairwise-generation`) when the full product is too large.

## Run it
- CI matrix builds:
  ```yaml
  strategy:
    matrix:
      os: [ubuntu-latest, windows-latest, macos-latest]
      python: ["3.10", "3.12", "3.13"]
  ```
- Containers: run tests inside the official image for each target; multi-arch images tested on arm64 runners (or QEMU, slower).
- Databases: Testcontainers with each supported DB version.

## What breaks
Path separators and case sensitivity, line endings, default encodings (Windows cp1252), time zone databases, arm64 native dependencies, file permissions, available system fonts, DB SQL dialect differences.

## Gotchas
- Declaring support for an environment that is never tested.
- Docker Desktop on macOS behaves differently from Linux hosts (file system speed, networking).

## Verify
Every supported environment in the documentation maps to a passing CI matrix cell or a recorded manual run for the release.

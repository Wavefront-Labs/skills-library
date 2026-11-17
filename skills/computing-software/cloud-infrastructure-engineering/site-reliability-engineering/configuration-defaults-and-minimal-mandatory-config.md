---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.configuration-defaults-and-minimal-mandatory-config
name: configuration-defaults-and-minimal-mandatory-config
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, configuration-design, config-defaults-design, configuration-philosophy, safe-defaults]
level: advanced
status: docs-checked
description: "Design configuration with safe defaults and minimal mandatory settings: what to require, dynamic defaults, user intent vs implementation knobs, and when to drop options."
sources: ["https://sre.google/workbook/configuration-design/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration defaults and minimal mandatory config

**Goal:** users configure what they care about; the system handles the rest safely.

## Principles (SRE Workbook, Configuration Design and Best Practices)
- Ask about **user intent** (what the user needs, in their terms), not exactly how the system should do it.
- Mandatory questions are those that must be answered for any function at all (the page's example: who to
  charge for an operation). Minimise them; the easiest way is to make them optional with a default that
  applies safely and effectively to most users (example: do a dry run by default).
- Optional questions improve quality of function but do not dictate core function (example: number of worker processes).
- Defaults can be **dynamic**: for example, as many computation threads as the system or container has
  cores, or a Java binary alone in a container adjusting heap limits to container memory. Keep the ability
  to override dynamic defaults when resource use must be restricted.
- Most users use the default, so a wrong default does a lot of harm; choose it carefully.
- In a configuration language with inheritance, leaf configurations should be able to revert any optional question to its default.

## Design steps
1. List every knob; classify as mandatory or optional.
2. Convert mandatory questions to optional ones with safe defaults where you can.
3. Remove optional questions that start without a clear use case; add knobs only for a real need.
4. Validate semantically at commit time (not only syntax), so misconfigurations are caught before submission.
5. Watch how dynamic defaults land: if a significant portion of users report problems, improve the logic broadly instead of adding knobs; if only a few are unhappy, manual options are fine.

## Anti-patterns
- Exposing many tunables "for flexibility": more knobs means more surface for error and more cognitive load.
- Lowest-common-denominator complexity as the default, which burdens even the simplest use cases.

## Verify
- [ ] A minimal example configuration with only the mandatory fields works as intended.

## Checked
2026-11-01. Confirmed against SRE Workbook chapter 14 (sre.google/workbook/configuration-design/): mandatory vs optional questions and examples, dry-run default, dynamic defaults, the harm of wrong defaults, inheritance revert, semantic validation at commit.
Removed: the 99.9% availability example, the data-retention and region examples, the effective-configuration, usage-statistics and deprecation-warning steps, and the "defaults safe only in dev" anti-patterns, because the chapter does not state them.
Method: documentation only; no commands were run.

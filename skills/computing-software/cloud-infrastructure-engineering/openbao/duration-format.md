---
id: computing-software.cloud-infrastructure-engineering.openbao.duration-format
name: duration-format
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, duration, ttl, units, config]
level: intro
status: docs-checked
description: "OpenBao duration strings: accepted units (ns to d), fractional values, and the seconds default when no unit is given."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/duration-format.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Duration format

A duration string is a possibly signed sequence of decimal numbers, each with optional fraction and unit suffix.

## Units

`ns`, `us` (or `µs`), `ms`, `s`, `m`, `h`, `d`.

## Examples from the docs

- `100` is 100 seconds
- `60h`, `1.5h`, `50d`, `100ms`, `50ns`

## Gotcha

With no unit, the number is read as seconds, so `3600` is one hour but a bare `30` is 30 seconds, not 30 minutes. Write the unit explicitly in configs and API calls.

The format applies wherever OpenBao accepts durations, in configuration and APIs; the telemetry option `usage_gauge_period` is one example.

## Checked

2026-11-04. Confirmed against the Duration string format page: signed decimal numbers with optional fraction and unit, unit list ns to d, seconds when no unit, the example values and the usage_gauge_period mention. Nothing removed.

Method: documentation only; no commands were run.

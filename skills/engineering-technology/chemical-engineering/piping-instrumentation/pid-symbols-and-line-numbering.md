---
id: engineering-technology.chemical-engineering.piping-instrumentation.pid-symbols-and-line-numbering
name: pid-symbols-and-line-numbering
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-pid-development, pid-symbols-and-line-numbering, pid-symbols, line-numbering, isa-5-1, instrument-tag]
level: practitioner
status: gated
description: "Apply P&ID symbols and a line numbering scheme: ISA-style instrument tags, equipment tags and line number fields."
sources:
  - "Crane Technical Paper 410, Perry Chemical Engineers Handbook, ASME B31.3, ISA-5.1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.isa.org"
  - "https://www.isa.org/standards-and-publications/isa-standards/isa-5-standard"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pid symbols and line numbering

**Goal:** Apply P&ID symbols and a line numbering scheme: ISA-style instrument tags, equipment tags and line number fields.

## Steps
1. Fix the company legend first; follow the ISA-5.1 tag convention (first letter measured variable, succeeding letters function (gated: unconfirmed, source is paywalled or blocked)) for instruments, for example FIC for a flow indicating controller.
2. Line numbers typically combine size, fluid service code, area or unit, sequence number and piping class (and insulation code); use the project line list format.
3. Show every line with its number, direction, size and class changes, and spec breaks.
4. Equipment tags follow a type letter plus unit and sequence number (for example P-101).
5. Keep one legend for the project and check the edition used by your company; ISA lists ANSI/ISA-5.1-2024 "Instrumentation and Control - Symbols and Identification" as current (isa.org).

## Gotchas
- Company standards override generic schemes; match the client format.
- Do not reuse tag numbers.

## Verify
- [ ] Every line and instrument is tagged uniquely.
- [ ] Legend covers all the symbols used.

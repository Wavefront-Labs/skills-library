---
id: computing-software.software-engineering.api-design.evolving-enums-and-unknown-values
name: evolving-enums-and-unknown-values
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, enum-evolution, api-evolution, aip-126, forward-compatibility, unknown-values]
level: practitioner
status: docs-checked
description: "Add enum values without breaking clients: UNSPECIFIED zero values, documented open enums, client handling of unknown values, and when a new value is a breaking change."
sources: ["https://google.aip.dev/126", "https://protobuf.dev/programming-guides/enum/", "https://github.com/OAI/OpenAPI-Specification/issues/1552"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evolving enums and handling unknown values

## Server/schema rules
- In protobuf the first value is the enum name plus `_UNSPECIFIED` (zero); AIP-126 allows a clearly useful zero such as an `UNKNOWN` value instead of having both.
- AIP-126: enums should get new values infrequently; for values that change often use a string and document the format.
- Document every enum as **open**: "new values may be added; clients must handle unknown values".
  Put that sentence in the field description and the API style guide.
- Adding a value is additive for **outputs only if clients were told it's open**. For an input
  enum it is always safe. Removing or renaming a value is breaking; deprecate it and keep accepting it.
- A new value that changes meaning of existing data (splitting `PAID` into `PAID` and
  `PAID_PARTIAL`) is breaking for clients that branch on it: ship behind a new API version or opt-in.
- Prefer enums over booleans when a third state is plausible; prefer a separate field over
  overloading an enum with orthogonal states.

## Client rules (put in SDK and docs)
- Deserialise unknown strings into an `UNKNOWN`/raw variant, never throw. Generated clients often
  fail here. openapi-generator has an `enumUnknownDefaultCase` property in several generators (java and typescript are named in the OpenAPI issue 1552 thread); or model as string + constants.
- Protobuf: proto3 and editions use open enums, which store an unknown number in the field; closed enums move it to the unknown field set. Java's getter returns `UNRECOGNIZED` for values outside the known set.
- `switch` statements must have a default branch that degrades (show "Other", skip the item).

## Verify
Contract test: inject an unseen enum value in a fixture response; every client parses it and the
UI shows a fallback.

## Checked
2026-11-01. Confirmed: AIP-126 (_UNSPECIFIED first value, UNKNOWN exception, infrequent additions), protobuf enum guide (open vs closed enums, Java UNRECOGNIZED), OpenAPI issue 1552 (enumUnknownDefaultCase). Removed: JSON-ints rule, generator-crash claim, TypeScript/Rust exhaustiveness advice.
Method: documentation only; no commands were run.

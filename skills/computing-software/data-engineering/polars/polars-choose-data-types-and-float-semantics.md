---
id: computing-software.data-engineering.polars.polars-choose-data-types-and-float-semantics
name: polars-choose-data-types-and-float-semantics
category: computing-software
field: data-engineering
product: polars
tags: [polars, polars-data-types, dtypes, null-vs-nan, float, decimal, list-vs-array, enum, struct]
level: practitioner
status: docs-checked
description: "Pick the right Polars data type from the full type table and know how NaN, null and floating point comparisons behave."
sources:
  - https://docs.pola.rs/user-guide/concepts/data-types-and-structures/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choose a Polars data type and understand float behaviour

Goal: map your data to the right dtype and avoid null versus NaN surprises.

## Categories

- Numeric: signed integers, unsigned integers, floats, decimals.
- Nested: lists, structs, arrays, maps.
- Temporal: dates, datetimes, times, time deltas.
- Misc: strings, binary, Booleans, categoricals, enums, objects.

All types support missing values as `null`. Do not conflate `null` with `NaN` in float types.

## Type table

| Type(s) | Notes from the docs |
| --- | --- |
| `Boolean` | bit packed efficiently |
| `Int8`..`Int128`, `UInt8`..`UInt128` | varying-precision signed and unsigned integers |
| `Float16`, `Float32`, `Float64` | varying-precision signed floats |
| `Decimal` | 128-bit with optional precision and non-negative scale; use when you need fine-grained control over precision |
| `String` | variable length UTF-8 |
| `Binary` | arbitrary raw bytes |
| `Date`, `Time`, `Datetime`, `Duration` | calendar date, time of day, both, and a duration |
| `Array` | fixed shape per series, akin to numpy arrays |
| `List` | homogeneous 1D container with variable length |
| `Object` | wraps arbitrary Python objects |
| `Categorical` | string encoding where categories are inferred at runtime |
| `Enum` | ordered encoding of predetermined string categories |
| `Struct` | composite type with multiple fields |
| `Map` | key-value mapping per row; keys unique within a row and never null; entry order preserved |
| `Null` | represents null values |

## Floating point rules

Polars follows IEEE 754 for `Float32` and `Float64`, with exceptions:

- Any `NaN` compares equal to any other `NaN`, and greater than any non-`NaN` value.
- No guarantee on the sign of zero or the payload of `NaN`. A sort or group by may canonicalize all zeroes to +0 and all `NaN`s to a positive `NaN` without payload for efficient equality checks.
- Results are reasonably accurate but no error guarantee is given unless stated; some error is always expected.

## Checked
2026-11-07: every claim compared with the cited Polars user guide page(s). No unconfirmed claims found.

Method: documentation only; no commands were run.

---
id: computing-software.firmware-embedded-development.iot-protocols.protobuf-schema-evolution
name: protobuf-schema-evolution
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [protobuf-schema-evolution, protobuf, schema-evolution, reserved, field-numbers, iot-protocols]
level: practitioner
status: docs-checked
description: "Protobuf schema evolution: wire-safe changes to field numbers, removals, enums, oneofs and types when old firmware must keep decoding."
sources:
  - https://protobuf.dev/programming-guides/proto3/
  - https://jpa.kapsi.fi/nanopb/docs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protobuf schema evolution

**Goal:** Evolve device messages without breaking firmware already in the field.

## Steps
1. Never reuse a field number, and never change an existing field's number (that equals deleting the field and adding a new one).
2. Removing a field is wire-safe, but reserve its number and name, or rename it with an OBSOLETE_ prefix.
3. Proto3 keeps unknown fields and includes them when parsing and serializing, so adding fields with new numbers is safe for readers. They can be lost via JSON or field-by-field copies; use binary format and CopyFrom/MergeFrom.
4. Use optional for scalars where you must tell unset from default. Implicit-presence scalars set to the default are not serialized.
5. Adding enum values is wire-safe but can break exhaustive switches. Reserve removed enum numbers; reused numbers corrupt data.
6. Oneof: moving existing singular fields into a oneof is wire-unsafe; moving one field into a new oneof is safe.
7. Compatible type swaps (may be lossy, out-of-range values truncate): int32, uint32, int64, uint64 and bool; sint32 with sint64; string with bytes if valid UTF-8; fixed32 with sfixed32; fixed64 with sfixed64; enum with int32/uint32/int64/uint64. Singular to repeated is generally unsafe for numeric types.
8. Do such type changes only with a managed rollout, not for schemas published outside your organisation.

## Gotcha
A reused field number or a reused enum number makes old firmware misread new data silently. Reserve numbers instead.

## Verify
- [ ] An old decoder reads a new message
- [ ] Removed numbers and names appear under reserved
- [ ] A field number registry or schema history is kept

## Checked

2026-11-08. Confirmed on the proto3 guide's "Updating a Message Type" material: field numbers, removal, unknown fields, presence, enums, oneof, type compatibility lists. Removed as unsupported: the claim that numbers 1 to 15 take a one-byte tag, a schema version field, and the buf breaking CI step (marked confirm in the old draft; not on the pages). The nanopb page does not discuss schema evolution; it notes that unknown fields are not preserved on decode and re-encode, which matters for gateways using nanopb.
Method: documentation only; no commands were run.

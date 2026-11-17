---
id: computing-software.software-engineering.api-design.protobuf-schema-design
name: protobuf-schema-design
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, grpc, protobuf, proto-design, protobuf-schema, field-numbers, proto3, well-known-types, field-presence, buf-lint]
level: practitioner
status: verified
description: "Design Protocol Buffers schemas for gRPC APIs: package/versioned naming, field numbering, presence and optional, enums with UNSPECIFIED, well-known types, and buf lint."
sources: ["https://protobuf.dev/programming-guides/proto3/", "https://protobuf.dev/programming-guides/dos-donts/", "https://protobuf.dev/best-practices/api/", "https://buf.build/docs/lint/rules/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protobuf schema design

**Goal:** .proto files that are pleasant to use from every language and can evolve for
years without breaking clients.

Checked with protoc (grpcio-tools 1.84, libprotoc 35.1) and buf 1.74: the schema below, with `Invoice` using `optional int32 limit`, `reserved 4; reserved "old_name"`, passes `buf lint` with the STANDARD rules (its default layout is one request and one response message per RPC); a bad file with an unversioned package, unresolved types and a lower-case enum was rejected. protoc errors observed: field numbers 19000-19999 (`Field numbers 19000 through 19999 are reserved for the protocol buffer library implementation`), `map` fields in a `oneof` or with `repeated` (both rejected), a first enum value that is not zero (`The first enum value must be zero for open enums`), a field using a reserved number or reserved name, and enum values sharing a name across enums in one package (enum values are siblings of their type, which is why values are prefixed with the enum name). In Python, `HasField` works for `optional` scalars (`False` until set, `True` after setting 0) and raises `ValueError` for a plain proto3 scalar.

## Layout and naming
```proto
syntax = "proto3";
package acme.billing.v1;                       // versioned package
option go_package = "github.com/acme/apis/gen/go/acme/billing/v1;billingv1";

service InvoiceService {
  rpc GetInvoice(GetInvoiceRequest) returns (Invoice);
  rpc ListInvoices(ListInvoicesRequest) returns (ListInvoicesResponse);
}
message GetInvoiceRequest { string name = 1; }   // "invoices/123" (AIP resource name)
```
- One request/response message per RPC (never reuse or use `Empty` for requests you
  may extend later; `google.protobuf.Empty` can't gain fields).
- Files `lower_snake_case.proto`, messages `PascalCase`, fields `lower_snake_case`,
  enums values `UPPER_SNAKE` prefixed with the enum name.

## Field numbers
- 1-15 encode in a one-byte tag, 16 and up need two (checked with the Python encoder): use 1-15 for frequent fields.
- Never reuse or renumber a field. Deleting a field: `reserved 4; reserved "old_name";`.
- 19000-19999 are reserved by protobuf.

## Presence and defaults
proto3 scalars have no presence: `0`, `""`, `false` are indistinguishable from "unset".
- Need to distinguish? Use `optional int32 limit = 3;` (generates has_limit) or a
  wrapper/message type.
- For partial updates use a `google.protobuf.FieldMask update_mask` (AIP-134) rather
  than relying on presence of every field.

## Enums
```proto
enum InvoiceState {
  INVOICE_STATE_UNSPECIFIED = 0;   // zero value must mean "unknown/unset"
  INVOICE_STATE_DRAFT = 1;
  INVOICE_STATE_PAID = 2;
}
```
Clients must handle unknown values (protobuf.dev: unrecognised enum values are preserved on deserialisation; how they show up is language-dependent).

## Types
- `google.protobuf.Timestamp` / `Duration` instead of int64 seconds; `google.type.Money`
  (googleapis, units + nanos) for money; never float for currency.
- `oneof` for mutually exclusive fields (protobuf.dev: moving fields into an existing
  `oneof` is not safe, some fields may be cleared on reserialisation; moving a single field into a
  new `oneof` is safe).
- `map<string, Value>` is fine but can't be repeated or used as oneof members.
- Avoid `google.protobuf.Any` in public APIs unless truly extensible; it weakens typing.

## Tooling
`buf lint` (rule sets STANDARD) enforces naming, package versioning and request/response
conventions; `buf format -w` formats; `buf generate` with a `buf.gen.yaml` replaces
hand-rolled protoc invocations.

## Verify
- [ ] `buf lint` clean.
- [ ] Every enum has an `_UNSPECIFIED = 0` value; every RPC has its own request/response messages.

---
id: computing-software.software-engineering.api-design.proto-evolution-and-breaking-change-detection
name: proto-evolution-and-breaking-change-detection
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, grpc, protobuf, proto-evolution, buf-breaking, wire-compatibility, reserved-fields, breaking-changes, schema-registry]
level: practitioner
status: gated
description: "Evolve protobuf APIs without breaking clients: wire vs source compatibility, safe and unsafe changes, reserved fields, and enforcing it with buf breaking in CI."
sources: ["https://protobuf.dev/programming-guides/proto3/#updating", "https://buf.build/docs/breaking/", "https://buf.build/docs/breaking/rules/", "https://google.aip.dev/180"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proto evolution and breaking-change detection

**Goal:** ship schema changes continuously while old clients and servers (and stored
messages) keep working.

Run here with buf 1.74.0 (`buf breaking --against '.git#branch=main'` on a scratch repo): a field type change, a field rename (also flagged as `json_name` change), a removed `reserved` range, a deleted RPC, a changed package and unary-to-streaming were all reported under FILE; adding a field and adding an enum value were not reported. Under the looser categories (`buf config ls-breaking-rules` lists FILE, PACKAGE, WIRE_JSON, WIRE and CSR): WIRE_JSON and WIRE still flagged type change, streaming change and a deleted field that was not reserved (WIRE_JSON wants both number and name reserved, WIRE only the number), WIRE_JSON flagged field and enum-value renames, but neither flagged a renamed RPC or a package rename. So looser categories do not protect method paths; keep FILE (or add PACKAGE and service rules) if clients call by `/pkg.Service/Method`. The remote `buf.build/...` form of `--against` was not run (gated: unconfirmed, source is paywalled or blocked).

## Kinds of compatibility
- **Wire**: old binaries can parse new messages and vice versa. Depends on field
  NUMBERS and types.
- **JSON**: also depends on field NAMES (proto3 JSON uses names).
- **Source/generated code**: renames break compile for users of generated code even if
  the wire is fine.
Decide which you promise; for public APIs, all three.

## Safe changes
- Add a new field with a new number (old readers skip unknown fields).
- Add an RPC, a message, an enum value (clients must handle unknown values).
- Add `optional`/`reserved`, deprecate with `[deprecated = true]`.

## Breaking changes
| Change | Why |
|---|---|
| Change a field's number or type (most) | wire misinterpretation |
| Reuse a deleted field number | old data decoded as the new field |
| Rename field | breaks JSON and generated code |
| Remove field without `reserved` | invites reuse later (buf WIRE and WIRE_JSON flag it; FILE flags any deletion) |
| Change `repeated` <-> singular (non-packed issues), move into/out of `oneof` | semantics |
| Rename package/service/RPC | breaks every client's method path (`/pkg.Service/Method`) |
| Change an RPC to/from streaming | different call shape |
Some type changes are wire-compatible (int32 <-> int64 <-> uint32 <-> bool truncation
rules) but still semantic traps; avoid.

## Removing a field properly
```proto
message User {
  reserved 3, 7 to 9;
  reserved "legacy_email";
  string name = 1;
}
```

## Enforce in CI
```yaml
# buf.yaml
version: v2
breaking:
  use: [FILE]        # strictest (generated code); WIRE_JSON or WIRE for looser promises
```
```bash
buf breaking --against '.git#branch=main'
buf breaking --against 'buf.build/acme/apis'     # against the published BSR module
```
Run on every PR touching protos; fail the build.

## Making truly breaking changes
New package version (`acme.billing.v2`), run v1 and v2 side by side, migrate clients,
then deprecate v1 with a timeline (AIP-185 API Versioning; AIP-180 covers backwards compatibility).

## Verify
- [ ] `buf breaking` runs in CI against the main branch.
- [ ] Deleted fields appear in `reserved` (numbers and names).

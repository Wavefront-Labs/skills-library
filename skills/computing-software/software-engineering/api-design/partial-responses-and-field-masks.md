---
id: computing-software.software-engineering.api-design.partial-responses-and-field-masks
name: partial-responses-and-field-masks
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, pagination, field-masks, sparse-fieldsets, partial-response, patch-semantics, aip-161]
level: practitioner
status: docs-checked
description: "Support partial responses (fields / sparse fieldsets) and partial updates with field masks (AIP-161, protobuf FieldMask), including PATCH semantics and nested paths."
sources:
  - https://google.aip.dev/161
  - https://google.aip.dev/134
  - https://protobuf.dev/reference/protobuf/google.protobuf/#field-mask
  - https://jsonapi.org/format/#fetching-sparse-fieldsets
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Partial responses and field masks

## Partial responses (read side)
Let clients ask for only the fields they need - smaller payloads, fewer expensive joins.
- JSON:API sparse fieldsets: `GET /articles?fields[articles]=title,body&fields[people]=name`. The value is a comma-separated list per type, and the endpoint must not include other fields of that type.
- GraphQL does this inherently.
Rules: default to a sensible representation when `fields` is absent; validate paths against the schema (400 on unknown); skip computing expensive fields when not requested (that is the performance win); keep `id` always present.

## Field masks for updates (write side)
PATCH with a full object is ambiguous: does a missing field mean "leave unchanged" or "clear it"? A field mask states exactly which fields to update.
```
PATCH /v1/books/1?update_mask=title,author.display_name
{"title": "The Dispossessed", "author": {"display_name": "Ursula K. Le Guin"}, "isbn": "ignored"}
```
- AIP-134: the mask field must be named `update_mask`, of type `google.protobuf.FieldMask`, and optional.
- If the mask is omitted, the service treats it as an implied mask of all populated (non-empty) fields.
- An empty mask (no paths) is a no-op that returns the existing resource.
- The special value `*` means full replacement (like PUT); it is an API-level convention that standard protobuf runtime helpers do not recognise, and AIP-134 says explicit fields are safest.
Protobuf/gRPC: `google.protobuf.FieldMask update_mask = 2;`.

## Alternatives for JSON APIs
JSON Merge Patch and JSON Patch are the usual JSON alternatives (not covered by this skill's sources); choose one and declare the media types.

## Pitfalls
- Output-only fields in a mask: AIP-161 says the service must ignore output-only fields provided as input, so one mask works for input and output.
- Repeated fields must be terminal elements in a path with standard protobuf utilities; services may support wildcards such as `authors.*.given_name` (AIP-161).
- Authorisation per field (some fields admin-only) must check the mask, not just the body.

## Verify
- [ ] Tests: field outside mask unchanged; empty mask is a no-op; unknown path rejected.
- [ ] Response size and DB queries drop when `fields` excludes expensive relations.

## Checked
2026-11-01. Confirmed: AIP-134 (update_mask name/type, implied mask, empty mask, `*`), AIP-161 (output-only fields ignored, repeated-field wildcards), JSON:API fields[TYPE]. Removed: X-Goog-FieldMask, Java/Go helper names, RFC 7396/6902 specifics, masked-absent-field-cleared and 400 claims.
Method: documentation only; no commands were run.

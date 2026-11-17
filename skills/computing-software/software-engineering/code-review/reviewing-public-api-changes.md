---
id: computing-software.software-engineering.code-review.reviewing-public-api-changes
name: reviewing-public-api-changes
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, specialised-review, api-review, breaking-change-review, semver, api-diff, naming, backward-compatibility-review]
level: advanced
status: draft
description: "Review changes to public APIs (HTTP, gRPC, library interfaces): compatibility, naming consistency, error semantics, versioning impact, docs and automated API-diff checks."
sources: ["https://google.aip.dev/180", "https://google.aip.dev/1", "https://github.com/microsoft/api-guidelines", "https://semver.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing public API changes

**Goal:** anything other teams or customers will code against gets extra scrutiny,
because mistakes there are permanent or costly to undo.

## Identify that it IS an API change
Public HTTP routes and payloads, protobuf/OpenAPI/GraphQL schemas, exported functions
and types in libraries, CLI flags and output formats that scripts parse, event schemas,
config file formats, database views consumed by others. Tag these paths in CODEOWNERS
so API reviewers are added automatically.

## Checklist
1. **Compatibility**: is anything removed, renamed, retyped, made required, or
   semantically changed? Run automated diffs: `buf breaking`, `oasdiff breaking`,
   GraphQL schema checks, `cargo semver-checks`, `apidiff`/`gorelease`, japicmp,
   `@microsoft/api-extractor`. If breaking, is the version bumped and a migration path given?
2. **Consistency** with the rest of the API: naming conventions, pagination style, error
   format, time/money representations, id formats. An API guide (Google AIPs, Microsoft
   REST guidelines, your own) is the reference; inconsistency is a legitimate blocker.
3. **Minimal surface**: does every new field/method/flag have a current use case? Exposing
   less is easier to extend than exposing more is to take back.
4. **Error semantics**: which errors/status codes can callers now receive; are they
   documented and distinguishable?
5. **Defaults and nullability**: what happens when the new field is absent (old clients)?
6. **Security**: authz on new endpoints/fields, data exposure (are we leaking internal ids
   or PII?), rate limits.
7. **Performance contract**: unbounded lists, N+1 traps for clients, payload size.
8. **Docs, examples and changelog** updated in the same PR.

## Process tips
- Prefer reviewing the schema/interface diff BEFORE the implementation (API-first PR or
  design doc), so implementation reviews don't relitigate the shape.
- Mark experimental surface explicitly (`v1beta`, `@Experimental`, `unstable` feature
  flags) so it can still change.

## Verify
- [ ] API diff tool output attached or run in CI for the PR.
- [ ] Every new public element is documented and consistent with the API style guide.

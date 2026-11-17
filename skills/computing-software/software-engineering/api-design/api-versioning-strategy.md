---
id: computing-software.software-engineering.api-design.api-versioning-strategy
name: api-versioning-strategy
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-versioning, versioning-strategy, url-versioning, header-versioning, date-based-versioning, stripe-versioning, media-type-versioning, version-pinning]
level: practitioner
status: docs-checked
description: "Choose an API versioning scheme (URL major version, date-based interface versions, per-account pinning) using Google AIP-185 and Stripe's published approach, and run versions."
sources: ["https://google.aip.dev/185", "https://stripe.com/blog/api-versioning", "https://docs.stripe.com/api/versioning"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API versioning strategy

**Goal:** be able to make the occasional breaking change without stranding clients,
while keeping the number of live versions small.

## Options as documented
| Scheme | Documented example |
|---|---|
| Major version in the URL path | AIP-185: every Google API interface must have a major version, encoded at the end of the protobuf package and as the first part of the REST path (`/v1/...`). Only the major number is exposed: `v1`, not `v1.0` or `v1.4.2`; minor/patch-equivalent changes update in place. |
| Stability suffix | AIP-185: alpha and beta append the level (`v1beta`, `v1alpha`; release-based `v1beta1`, `v1alpha5`); the stable channel never carries a suffix. |
| Date-based interface versions | AIP-185 interface-based versioning: stable versions are `YYYY-MM-DD`, previews `YYYY-MM-DD-preview`. |
| Per-account pinned version with header override | Stripe: the account's pinned version is set on its very first request, and a `Stripe-Version` header overrides it per request. |

Default: major version in the URL plus additive evolution within a version (see
computing-software.software-engineering.api-design.tolerant-reader-and-additive-change); consider date-based
pinning only if you expect frequent, granular breaking changes and can fund the machinery.

## Running date-based versions (Stripe's blog)
- Resources are written for the current version; each backwards-incompatible change lives in a "version change
  module" holding documentation, a transformation and the set of eligible resource types.
- Older pinned versions are served by applying those transformations to the current response.
- Some changes have side effects beyond the response and are flagged `has_side_effects`; their transformation
  is a no-op.
- Reference docs can be tailored to the logged-in account's version.

## Policies to write down
- What counts as breaking and what is additive (AIP-180, linked above).
- A new major version must not depend on a previous major version of the same API (AIP-185).
- Support window and turn-down process, defined up front (AIP-181).

## Anti-patterns
- Exposing minor or patch versions in URLs: AIP-185 forbids it for Google APIs, since they update in place.

## Checked
Date: 2026-11-01. Confirmed on AIP-185 (major version rule, no minor or patch, stability suffixes, date formats,
independence of major versions), Stripe's API versioning blog (pinning on first request, version change modules,
side effects, tailored docs) and Stripe API versioning docs (Stripe-Version header override). Removed: the
Azure query-parameter row and media-type row (not confirmed on a fetched page), RFC 9745 and RFC 8594 header
claims, example 12-month window, per-endpoint versioning advice and the verification list.
Method: documentation only; no commands were run.

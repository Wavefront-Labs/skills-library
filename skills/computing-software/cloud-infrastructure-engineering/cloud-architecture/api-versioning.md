---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.api-versioning
name: api-versioning
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, api-gateway-patterns, api-versioning, breaking-changes, deprecation-policy, sunset-header, semantic-versioning-apis]
level: practitioner
status: docs-checked
description: "Version APIs without breaking consumers: date-based api-version vs major version in path, extensible enums, and the Deprecation and Sunset response headers."
sources: ["https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md", "https://www.rfc-editor.org/rfc/rfc8594", "https://datatracker.ietf.org/doc/html/rfc9745", "https://google.aip.dev/185"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API versioning

## Breaking vs non-breaking
- Azure guidelines: do not introduce breaking changes into a service without approval; removing a value from an
  enum is breaking, and adding paging to a list later is breaking.
- Adding a value to an enum is safe only if the enum is extensible (a string marked `modelAsString: true` in an
  `x-ms-enum` block), so clients must tolerate unknown values.
- Changing the top-level error code returned for the same conditions is a breaking change.

## Schemes
| Scheme | Example | Source |
|---|---|---|
| Required query parameter, date value | `?api-version=2021-06-04` (`YYYY-MM-DD`, `-preview` suffix for previews) | Azure guidelines |
| Major version in URI path | `/v1/...`; Google APIs use `v1`, never `v1.1` | AIP-185 |
| Version header or query parameter | `X-Goog-Api-Version` header or `$apiVersion` query parameter, date-valued | AIP-185 interface-based versioning |

- Azure: return 400 `MissingApiVersionParameter` when the parameter is absent and 400 `UnsupportedApiVersionValue`
  for an unknown value, listing the supported stable versions and the latest preview. A GA version must use a later
  date than its preview version.
- Google (channel-based): the stable channel has no suffix (`v1`); alpha and beta append it (`v1beta`). Multiple
  versions must work at once for a reasonable transition period, and an older version goes through a well-communicated
  deprecation period before shutdown. AIP-185 recommends 180 days for beta functionality.

## Deprecation
1. Announce with a timeline and a deprecation period; Azure requires lengthy communication before any approved
   breaking change.
2. Send `Deprecation: @<unix-timestamp>` (RFC 9745, a Structured Field date) and, when removal is planned,
   `Sunset: <HTTP-date>` (RFC 8594). The Sunset time must not be earlier than the Deprecation time.
3. Send `Link: <url>; rel="deprecation"` to documentation about the deprecation (RFC 9745); RFC 8594 also defines a
   `sunset` link relation.
4. Deprecation does not change resource behaviour; the header is a hint. Azure uses an `azure-deprecating` response
   header, only with approval and an official deprecation notice.
5. Track usage per version and per consumer so laggards can be contacted (team practice).

## Verify
- [ ] Every operation requires or routes by a version, and unknown versions get a clear error.
- [ ] Deprecated versions send `Deprecation` and `Sunset` with a doc link.
- [ ] Usage per version dashboard.

## Checked
2026-11-08. Confirmed against the Azure REST API guidelines (api-version rules, error codes, extensible enums,
breaking-change notes, azure-deprecating), RFC 9745 (Deprecation header, link relation, Sunset ordering, examples),
RFC 8594 (abstract and introduction read; Sunset header and link relation) and Google AIP-185 (read in full). Removed
unsupported claims: the >= 12 months figure, the `Api-Version` header and media-type rows, the API gateway version
sets and stage mapping advice, brownouts, the "CI breaking-change detector" check and the generic breaking-change
list. Usage tracking is team practice, not a vendor claim.
Method: documentation only; no commands were run.

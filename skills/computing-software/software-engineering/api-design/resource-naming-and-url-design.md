---
id: computing-software.software-engineering.api-design.resource-naming-and-url-design
name: resource-naming-and-url-design
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, rest, resource-naming, url-design, aip-122, hierarchical-resources, uri-templates]
level: practitioner
status: docs-checked
description: "Name REST resources and design URLs: plural collection nouns, resource IDs, casing, allowed characters, action suffixes and stable resource names."
sources:
  - https://google.aip.dev/122
  - https://google.aip.dev/123
  - https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource naming and URL design

## Rules that hold up
- **Collections are plural nouns**, and a resource is identified by an ID within its collection: `/customers`, `/customers/{customer_id}`. AIP-122: collection identifiers are plural, camelCase, start with a lowercase letter and use only ASCII letters and digits; where singular and plural are the same ("info", "moose") do not coin a plural. A collection identifier may appear only once in a single name (`people/xyz/people/abc` is invalid).
- **Resource names** alternate collection identifiers and resource IDs, separated by `/` (`publishers/123/books/les-miserables`), and are unique within the API. Resources expose the name in a `name` field; do not call other fields `name`.
- **IDs:** user-specified IDs should follow RFC 1034 style (letters, digits, hyphen; first character a letter, last a letter or digit; 63 characters at most), lowercase only (`^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$`), and the allowed format must be documented. Names should avoid characters needing URL-escaping and non-ASCII characters. All ID fields should be strings.
- **Casing (Azure guidelines):** use kebab-casing for URL path segments (preferred) or camelCase; if the segment refers to a JSON field use camelCase. Treat service-defined path segments as case-sensitive.
- **Characters (Azure guidelines):** restrict service-defined path segments to `0-9 A-Z a-z - . _ ~`, with `:` allowed only to mark an action; keep user-specified path values to the same set without `:`. Keep URLs readable and avoid UUIDs and percent-encoding where possible. Return 414 for URLs over 2083 characters.
- **Aliases:** an alias such as `users/me` for the authenticated user is allowed (AIP-122), but data returned by the API must use the canonical resource name.
- **Hierarchy:** a resource has at most one canonical parent (AIP-124). Use nesting for ownership (`/customers/{id}/addresses/{address_id}`); use top-level collections plus filters for independent resources.
- **Do not hide actions in the path of standard operations.** Where a standard create, read, update, delete or list fits, use it. For other actions Azure uses a POST to `.../<resource-collection>:<action>` with a verb as the action (for example `users:grant`) and disallows `:` in resource IDs; AIP-164 uses the same `:undelete` style.
- **Full resource name:** `//library.googleapis.com/publishers/123/books/les-miserables` (service name plus relative name) is used only to refer to resources across multiple APIs where ambiguity is possible; it omits the API version.

## Resource types (AIP-123)
Type names are `{Service Name}/{Type}`, where the type matches the message name, is singular, PascalCase and alphanumeric. Pattern variables are snake_case with no `_id` suffix and match the singular of the type (`{topic}`); collection segments match the plural.

## Verify
- [ ] Every path in the OpenAPI document reviewed against these rules during API review.
- [ ] A lint ruleset in CI (for example Spectral with a custom ruleset) enforces casing and plural collections.

## Checked
2026-11-08. Read in full: AIP-122 and AIP-123. The Azure REST API Guidelines were read only in part (the URL structure and action-operation sections); claims taken from them are limited to those sections. Removed as unsupported: nesting limit of 2-3 levels, UUID/ULID/Stripe-style ID advice and enumeration arguments, query-vs-path table, secrets in URLs, `/documents/42/content`, trailing-slash and file-extension anti-patterns, versions in paths, and the RFC 3986 source (not read for this skill). The Spectral line is only a suggestion; no ruleset was checked.
Method: documentation only; no commands were run.

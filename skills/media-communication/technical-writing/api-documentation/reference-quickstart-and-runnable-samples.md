---
id: media-communication.technical-writing.api-documentation.reference-quickstart-and-runnable-samples
name: reference-quickstart-and-runnable-samples
category: media-communication
field: technical-writing
product: api-documentation
tags: [api-documentation, api-docs, developer-documentation, api-reference, openapi, swagger, redoc, quickstart, getting-started, code-samples, runnable-samples, curl, sdk, authentication, error-codes, pagination, rate-limits, changelog, versioning, deprecation, diataxis, docs-testing, postman, developer-experience]
level: practitioner
status: docs-checked
description: "Document an API so developers succeed: Diataxis doc types, a quickstart, OpenAPI-driven reference fields, samples kept as real files, and deprecation with Sunset."
sources: ["https://spec.openapis.org/oas/latest.html", "https://diataxis.fr/", "https://diataxis.fr/tutorials/", "https://diataxis.fr/reference/", "https://datatracker.ietf.org/doc/html/rfc8594"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API reference, quickstart and runnable samples

**Goal:** a developer goes from "never seen this API" to a successful authenticated call
quickly, can look up any endpoint precisely, and trusts that changes are announced. API
*design* itself: see
`computing-software.software-engineering.api-design.rest-resource-design-and-versioning`.

## 1. The four doc types (do not mix them)
Diataxis identifies four needs and four corresponding forms: **tutorials**, **how-to
guides**, **technical reference** and **explanation**.
- A tutorial is learning-oriented: a practical activity, under guidance, in which the
  student learns by doing something meaningful towards an achievable goal. A quickstart
  is this form.
- Reference is led by the product it describes, not by the user's needs: it describes,
  and only describes, as succinctly and in as orderly a way as possible. It should be
  austere; one consults reference rather than reads it. Explaining, instructing and
  opining run counter to what reference needs (accuracy, precision, completeness, clarity).
- API documentation is reference material that can be generated from the software it
  describes, which helps keep it faithful to the code.

## 2. The quickstart
1. Prerequisites in one list (account, key, language version).
2. Get credentials, and say where to put the key (environment variable, never in code).
3. **One copy-pasteable request**:
   ```bash
   export API_KEY=<YOUR_API_KEY>
   curl -s https://api.example.com/v1/widgets -H "Authorization: Bearer $API_KEY"
   ```
4. Show the actual expected response (trimmed) so the reader knows it worked.
5. Link to the most common how-to guides.
Test it with someone who has never used the API.

## 3. Reference pages from OpenAPI
Keep an OpenAPI description as the source of truth. The OpenAPI Specification provides
fields to document each operation and parameter:
- Operation `summary` (a short summary of what the operation does) and `description`
  (a verbose explanation of behaviour), with `deprecated` (boolean, default false)
  declaring an operation deprecated.
- Parameters: `description`, `required` (mandatory flag; always true for path
  parameters), `deprecated`, and `style` for serialisation.
- Request body: `description` and `required` (defaults to false); responses are
  documented per status code.
- Descriptions can use CommonMark.
Field descriptions should say what a field means and its units or format, not only its
type: `amount - integer, minor currency units (cents)`.

## 4. Cross-cutting pages
Authentication, errors (format and a table of codes), pagination, rate limits, webhooks
and a versioning policy each deserve a page.

## 5. Samples
- Keep samples as real files in the repository and include them in pages at build time.
- Run them in CI against a test environment; a failing sample fails the build.
- Use fake data and consistent `<ANGLE_BRACKET>` placeholders.

## 6. Changelog and deprecations
- Dated changelog entries, with breaking changes marked clearly and migration steps.
- Announce deprecations with a removal date and mark them in the reference
  (`deprecated: true` in OpenAPI).
- The `Sunset` HTTP response header field (RFC 8594) indicates that a URI is likely to
  become unresponsive at a specified point in the future.

## Gotchas
- A wrong spec produces confidently wrong docs; test the spec against the API.
- Real-looking keys in examples get flagged by secret scanners or copied into production.

## Verify
- [ ] Quickstart gives a runnable first call and the expected response.
- [ ] Every operation has summary, description, parameters and documented responses.
- [ ] Samples execute in CI.
- [ ] Errors, auth, pagination and rate-limit pages exist.
- [ ] Breaking changes have a dated changelog entry with migration steps.

## Checked
2026-11-09. Confirmed against the Diataxis home, tutorials and reference pages, the OpenAPI Specification latest (summary, description, deprecated, parameter required/deprecated/style, request body required, CommonMark) and RFC 8594 (Sunset header). Removed unconfirmed claims: the 5-minute quickstart target, tool names (Redoc, Spectral), the Deprecation header, changelog category names, and error/rate-limit page specifics.
Method: documentation only; no commands were run.

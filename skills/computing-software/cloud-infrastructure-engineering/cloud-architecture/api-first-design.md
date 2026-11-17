---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.api-first-design
name: api-first-design
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, information-systems-architecture, api-first-design, openapi, asyncapi, contract-first, api-guidelines, api-governance, schema-registry]
level: practitioner
status: docs-checked
description: "Run contract-first API design: OpenAPI and AsyncAPI descriptions written and reviewed before code, a published style guide, idempotency and long-running operation rules."
sources: ["https://spec.openapis.org/oas/latest.html", "https://www.asyncapi.com/docs/reference/specification/latest", "https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API strategy and contract-first design

## Steps
1. **Style guide**: adopt a published one (the Microsoft Azure REST API guidelines, or Google AIP) and record
   deviations: naming, paging, errors, versioning, idempotency, long-running operations.
2. **Write the contract first**: an OpenAPI Description for HTTP APIs and an AsyncAPI document for message-driven
   APIs. Keep it in the repo with the service and review it in pull requests with a consumer present (team practice).
3. **Describe the API in the contract, not in code comments**: OpenAPI is a language-agnostic interface description
   from which documentation, client and server code and test tooling can be produced; AsyncAPI is protocol-agnostic
   (AMQP, MQTT, WebSockets, Kafka, HTTP and others) and files are named `asyncapi.yaml` or `asyncapi.json` by convention.
4. **Apply the style guide's operational rules**, for example the Azure guidelines: all HTTP methods are idempotent
   (PUT or PATCH preferred for create; POST needs the Repeatability headers or equivalent), and operations that
   complete asynchronously return 202 Accepted and follow the long-running operation guidance.
5. **Versioning policy**: pick one scheme, publish deprecation timelines and use `Deprecation` and `Sunset` headers
   (see api-versioning).
6. **Catalogue**: publish specs with an owner and lifecycle (team practice).

## Gotchas
- Check which specification version your tools support: the current OpenAPI page is version 3.2.1, and the
  `openapi` field in each document states its version; the `info.version` field is the version of the document, not of the
  specification.
- Code-first annotations drifting from what is documented.
- Specs without examples; consumers guess (team practice).

## Verify
- [ ] The contract exists and is reviewed before implementation starts.
- [ ] The `openapi` or `asyncapi` field matches the version your tooling supports.
- [ ] Every public API is catalogued with owner and version.

## Checked
2026-11-08. Confirmed against the OpenAPI Specification latest page (v3.2.1: language-agnostic description, uses
for documentation, code generation and testing, version fields), the AsyncAPI specification latest page (v3.1.0:
protocol-agnostic, file naming) and the Azure REST API guidelines (idempotency, 202 for async operations). Removed
unsupported claims and the dead Stoplight Spectral source: Spectral linting, Prism and WireMock mocks, oasdiff
and openapi-diff, Pact and Schemathesis, schema registry compatibility modes, RFC 9457 and the OpenAPI 3.1 and
AsyncAPI 3 version pins. Review, catalogue and example advice is team practice, not a vendor claim. The OpenAPI
page was read for the introduction and field tables, not end to end.
Method: documentation only; no commands were run.

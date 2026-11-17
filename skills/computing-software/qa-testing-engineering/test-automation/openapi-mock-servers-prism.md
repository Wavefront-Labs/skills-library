---
id: computing-software.qa-testing-engineering.test-automation.openapi-mock-servers-prism
name: openapi-mock-servers-prism
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [prism-mock, mock-server, service-virtualization, openapi, contract-first, mockserver]
level: practitioner
status: verified
description: "Spin up mock servers from OpenAPI specs with Prism (static and dynamic examples, request validation) or MockServer, for parallel front-end and consumer development."
sources:
  - https://stoplight.io/open-source/prism
  - https://github.com/stoplightio/prism
  - https://www.mock-server.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenAPI mock servers (Prism, MockServer)

**Goal:** a mock of an API that does not exist yet, or cannot be used in tests, derived from its contract.

## Prism
```bash
npx @stoplight/prism-cli mock openapi.yaml            # static: returns spec examples
npx @stoplight/prism-cli mock -d openapi.yaml         # dynamic: generates data from schemas
```
- Validates requests against the spec: invalid requests get 422 with a `validation` array (Prism 5.16.0: a body missing a required property and a non-integer path parameter both returned 422 Unprocessable Entity), so consumers find contract violations early.
- Choose a response: `Prefer: code=404` or `Prefer: example=outOfStock` header (both worked; the example name is the key under `examples` in the spec). Dynamic mode (`-d`) returned random values, including negative integers and extra generated properties, which is why UI assumptions break.
- **Validation proxy**: `prism proxy openapi.yaml https://api.staging.example.com` (positionals `<document> <upstream>`, `-p` port) forwards to the real API and reports where requests or responses violate the spec: an upstream returning `{"id":"abc"}` produced a `sl-violations` response header and `Violation: response.body.id ... must be integer` log lines, while the response itself was still passed through with 200.

## MockServer
Expectations via REST/Java client, request verification, proxying and recording; Docker `mockserver/mockserver` (image name from the MockServer docs; not run here, no Docker). Good for complex matching and verification in Java tests.

## Use cases
- Front-end built in parallel with backend.
- Consumer tests isolating from flaky third parties.
- Spec conformance checking with Prism proxy in a staging pipeline.

## Gotchas
- Spec examples are often unrealistic or missing; dynamic mode generates random data that may break UI assumptions (very long strings). Add good examples to the spec.
- Mocks do not implement business logic or state; for stateful flows use WireMock scenarios or a fake.

## Verify
Running the consumer's tests against Prism shows zero request validation errors.

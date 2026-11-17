---
id: computing-software.software-engineering.api-design.client-sdk-generation
name: client-sdk-generation
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, api-contracts, sdk-generation, openapi-generator, openapi, client-libraries, code-generation]
level: practitioner
status: draft
description: "Generate client SDKs from OpenAPI/protobuf: openapi-generator vs Kiota vs commercial tools, spec hygiene for good output, versioning, publishing and customisation."
sources:
  - https://openapi-generator.tech/docs/usage
  - https://learn.microsoft.com/en-us/openapi/kiota/overview
  - https://buf.build/docs/generate/overview
  - https://github.com/OpenAPITools/openapi-generator
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Client SDK generation

## Tool options
| Tool | Notes |
|---|---|
| openapi-generator (`openapitools/openapi-generator-cli`) | 50+ languages, template-customisable; output quality varies by generator |
| Kiota (Microsoft) | builder-style fluent clients, consistent across languages, used for Microsoft Graph |
| oapi-codegen (Go), openapi-typescript + openapi-fetch (TS), NSwag (.NET), openapi-python-client | language-specific, often more idiomatic |
| Stainless, Speakeasy, Fern | commercial; idiomatic SDKs with pagination, retries, docs |
| buf generate / protoc plugins | gRPC/Connect clients from protobuf |

## Spec hygiene determines SDK quality
- Every operation has a unique, meaningful `operationId` (`listOrders`, `cancelOrder`) - it becomes the method name.
- Named schemas in `components/schemas` (not inline objects) so types get good names.
- Use `tags` to group operations into SDK services/classes.
- Model enums, `oneOf` with a `discriminator`, nullable vs optional correctly (OpenAPI 3.1 `type: [string, "null"]`).
- Declare security schemes, servers, pagination patterns, and error responses (problem details schema) so generators can type errors.
- Lint the spec first: `spectral lint openapi.yaml`, `redocly lint`.

## Generating
```bash
docker run --rm -v "$PWD:/local" openapitools/openapi-generator-cli generate \
  -i /local/openapi.yaml -g typescript-fetch -o /local/sdk/ts \
  --additional-properties=npmName=@acme/orders-client,supportsES6=true,useSingleRequestParameter=true
```
Pin the generator version (`openapitools.json` / Docker tag); upgrades change output. Use `.openapi-generator-ignore` to protect hand-written files.

## What generated clients usually lack
Retries with backoff, pagination iterators, idempotency key injection, auth token refresh, telemetry headers (`User-Agent: acme-orders-ts/1.4.0`). Add them via a thin hand-written wrapper or custom templates, not by editing generated code.

## Release process
- Generate in CI from the spec on each API release; run SDK tests against a mock (Prism `prism mock openapi.yaml`) or a sandbox.
- SemVer the SDK independently; a breaking API change or generator change that alters signatures is a major bump. Run `oasdiff breaking` on the spec to catch it early.
- Publish to npm/PyPI/Maven Central/NuGet with changelogs; deprecate old versions with notices.

## Verify
- [ ] Generated SDK compiles and its smoke tests pass in CI for every spec change.
- [ ] No hand edits inside generated directories (diff after regeneration is empty).

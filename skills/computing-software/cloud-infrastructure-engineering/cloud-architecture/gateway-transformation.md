---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.gateway-transformation
name: gateway-transformation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, gateway-patterns, gateway-transformation, api-gateway, protocol-translation, header-manipulation, payload-mapping]
level: practitioner
status: draft
description: "Transform requests and responses at the gateway: header and path rewrites, payload mapping, protocol translation (REST-gRPC, SOAP), versioning shims, and keeping logic thin."
sources: ["https://learn.microsoft.com/azure/api-management/api-management-transformation-policies", "https://docs.aws.amazon.com/apigateway/latest/developerguide/models-mappings.html", "https://docs.konghq.com/hub/kong-inc/request-transformer/", "https://cloud.google.com/apigee/docs/api-platform/reference/policies/assign-message-policy", "https://github.com/grpc-ecosystem/grpc-gateway"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Request and response transformation

## Steps
1. **Use transformation for compatibility, not business logic**: header injection and removal,
   path rewrites, legacy version shims, format translation for clients you cannot change.
2. **Headers**: add correlation IDs (`traceparent`), forward client identity claims as trusted
   headers after stripping any client-supplied copies, remove server-revealing headers
   (`Server`, `X-Powered-By`).
3. **Paths and versions**: map `/v1/orders/{id}` to the backend's new route; serve an old
   version by transforming to the new contract during deprecation.
4. **Payloads**: APIM `set-body` with Liquid templates or `json-to-xml`/`xml-to-json`; API
   Gateway REST mapping templates (VTL); Apigee AssignMessage/JSONtoXML; Kong
   request-transformer. Keep templates in source control with tests using sample payloads.
5. **Protocol translation**: REST to gRPC via Envoy gRPC-JSON transcoder or grpc-gateway;
   SOAP fronting with APIM SOAP-to-REST import; WebSocket to backend HTTP via API Gateway routes.
6. **Error mapping**: normalise backend errors into a standard format (RFC 9457 problem
   details) without leaking stack traces.
7. **Performance**: transformations buffer bodies; check payload size limits and added latency.

## Gotchas
- Logic hidden in gateway templates is hard to test and debug; when it grows, move it to a
  BFF or adapter service.
- Body transformation disables streaming for large responses.
- Trusting identity headers is safe only if the backend is reachable solely via the gateway.

## Verify
- [ ] Transformation tests run in CI against sample requests and responses.
- [ ] Backend is not reachable bypassing the gateway (network policy / private link).

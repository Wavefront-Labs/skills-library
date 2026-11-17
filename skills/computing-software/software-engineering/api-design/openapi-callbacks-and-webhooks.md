---
id: computing-software.software-engineering.api-design.openapi-callbacks-and-webhooks
name: openapi-callbacks-and-webhooks
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, openapi, openapi-callbacks, webhooks, callback-object, runtime-expressions, openapi-3-1]
level: practitioner
status: docs-checked
description: "Document outgoing webhooks and subscription callbacks in OpenAPI 3.1 using the webhooks field and operation callbacks with runtime expressions."
sources: ["https://spec.openapis.org/oas/v3.1.0", "https://learn.openapis.org/examples/v3.1/webhook-example.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenAPI callbacks and webhooks

Two constructs, for two situations.

## `webhooks` (top-level field in 3.1): events not tied to a client request
```yaml
openapi: 3.1.0
webhooks:
  orderShipped:
    post:
      requestBody:
        content: { application/json: { schema: { $ref: '#/components/schemas/ShippedEvent' } } }
      responses:
        '204': { description: Receiver acknowledges }
```
Use for fixed events the consumer registers for out of band (dashboard setup).

## `callbacks`: the URL arrives in the request
```yaml
paths:
  /subscriptions:
    post:
      requestBody:
        content: { application/json: { schema: { type: object, properties: { callbackUrl: { type: string, format: uri } } } } }
      callbacks:
        onEvent:
          '{$request.body#/callbackUrl}':
            post:
              requestBody: { content: { application/json: { schema: { $ref: '#/components/schemas/Event' } } } }
              responses: { '200': { description: OK } }
      responses: { '201': { description: Subscribed } }
```
The key is a runtime expression evaluated against the request/response that created the subscription, for example `{$request.body#/callbackUrl}`, `{$request.query.url}`, `{$response.header.Location}`, `$method`, `$url`. Expressions can be embedded in a larger string (`http://host?id={$request.body#/id}`). A callback value is a Path Item Object (or a reference to one).

## Gotchas
- The spec uses `webhooks` for incoming requests from the API provider that are independent of another API call, and `callbacks` for out-of-band requests tied to a parent operation. A document may contain only `webhooks`, `paths` or `components`; `paths` is no longer required.
- These objects describe messages; the spec has no field for signatures, retries or ordering, so write those in the description.
- Test delivery separately; a spec document does not send anything.

Verify: lint the file, render it with your docs tool and confirm the webhook or callback appears with its payload schema; add a contract test that your sender's payload validates against that schema.

## Checked
2026-11-08. Confirmed in the OpenAPI 3.1.0 specification (Callback Object section including key expressions and examples read in full; the document definition and `webhooks` mentions searched) and the learn.openapis.org webhook example (read in full). Removed: "webhooks is 3.1 only / absent in 3.0.x" and the standard-webhooks reference (not in the sources), the claim that mock servers rarely fire callbacks, and the Redoc/Scalar rendering assumption.
Method: documentation only; no commands were run.

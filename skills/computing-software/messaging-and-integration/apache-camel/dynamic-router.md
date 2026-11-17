---
id: computing-software.messaging-and-integration.apache-camel.dynamic-router
name: dynamic-router
category: computing-software
field: messaging-and-integration
product: apache-camel
tags: [apache-camel, eip, dynamic-router, null-termination, state]
level: advanced
status: docs-checked
description: "Camel Dynamic Router EIP: expression called until it returns null, option defaults, thread-safety warning and state in exchange properties."
sources:
  - https://camel.apache.org/components/next/eips/dynamicRouter-eip.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic Router

The expression is called iteratively to compute the next endpoint(s). Routing ends when it returns `null`. The page warns it must eventually return `null`, otherwise routing repeats endlessly.

Options (defaults): `uriDelimiter` `,`; `ignoreInvalidEndpoints` false (invalid URIs logged and skipped); `cacheSize` 1000 (`-1` disables); `allowedSchemes` unset (any); `disabled` false (cannot be re-enabled at runtime); `expression` required.

With the `@DynamicRouter` annotation the method returns the next endpoint URI, or `null` to finish; several endpoints are comma-separated.

The page text says `Exchange.SLIP_ENDPOINT` holds the current slip and shows how far routing has progressed; the generated properties table lists no exchange properties for this EIP.

Gotchas:
- The example bean is not thread-safe. Keep state in Exchange properties, which survive routing.
- Headers can carry state but are not guaranteed to survive.
- Output body is unknown.

Compare Routing Slip, which computes its whole list once before routing.

Verify: a bean that returns `direct:a`, then `direct:b`, then `null` visits a and b once each and ends.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full Dynamic Router EIP page source (dynamicRouter-eip.adoc) and the Dynamic Router model definition (dynamicRouter.json) from the apache/camel repository, which generate the cited page. Confirmed null termination and the endless-loop warning, option defaults (uriDelimiter, ignoreInvalidEndpoints, cacheSize 1000 and -1, allowedSchemes, disabled), the @DynamicRouter annotation, thread-safety and exchange-property state, headers not guaranteed to survive, unknown output body, and the contrast with Routing Slip. Reworded the SLIP_ENDPOINT note to report the conflict between the page text and the properties table instead of pointing at the implementation. No commands were run.

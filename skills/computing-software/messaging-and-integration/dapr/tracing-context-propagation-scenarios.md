---
id: computing-software.messaging-and-integration.dapr.tracing-context-propagation-scenarios
name: tracing-context-propagation-scenarios
category: computing-software
field: messaging-and-integration
product: dapr
tags: [tracing, trace-context, w3c, traceparent, service-invocation, pubsub, propagation, opentelemetry]
level: advanced
status: docs-checked
description: "Who propagates trace headers in Dapr: single calls are automatic, chains of three services and fan-out calls need your app to forward context, plus self-generated options."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/observability/tracing/tracing-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tracing applies to the service invocation and pub/sub APIs. Dapr generates trace context in the first sidecar of a request; whether you must forward it depends on the call shape.

- A to B (one Dapr invocation): Dapr generates headers in A and delivers them to B. Nothing else to do.
- A to B to C: Dapr covers A to B, but B must take the headers it received and send them on when it calls C through Dapr. Dapr always propagates a span to an application, but if the app calls Dapr and wants to continue an existing trace it must pass the header back in.
- External gateway to A: the ingress calls Dapr, which generates headers and calls A; A must forward them to B.
- One service calling several (A calls B, then C, then D): the trace headers come back to A in B response headers; Dapr does not know you want to reuse them, so your code must propagate the returned context to C and D.
- Pub/sub: Dapr generates headers on the published message topic; for `rawPayload` messages you can set the `traceparent` header yourself to carry context to subscribers.

The Dapr SDKs expose no helpers to propagate or read trace context, so use your HTTP or gRPC client to forward HTTP headers or gRPC metadata.

If you generate context yourself (for example from a non-Dapr app), Dapr still propagates it. Three ways: the standard OpenTelemetry SDK (the page calls this the preferred method), a vendor SDK that emits W3C trace headers, or a hand-built W3C trace context header. Dapr uses OTEL and Zipkin protocols, and OTEL is recommended.

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; wording tightened where it went beyond the page, the remaining claims are unchanged.

Method: documentation only; no commands were run.

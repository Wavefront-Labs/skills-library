---
id: computing-software.web-development.nextjs.instrumentation-and-opentelemetry
name: instrumentation-and-opentelemetry
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, nextjs-instrumentation, opentelemetry, vercel-otel, onrequesterror, observability, tracing, web-development]
level: practitioner
status: verified
description: "Instrumenting Next.js: instrumentation.ts register(), OpenTelemetry with @vercel/otel or the Node SDK, onRequestError reporting and client instrumentation."
sources:
  - https://nextjs.org/docs/app/guides/instrumentation
  - https://nextjs.org/docs/app/guides/open-telemetry
  - https://nextjs.org/docs/app/api-reference/file-conventions/instrumentation
  - https://opentelemetry.io/docs/languages/js/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instrumentation and OpenTelemetry in Next.js

**Goal:** traces for every request, server component render and fetch, plus centralised server error reporting.

## 1. instrumentation.ts
At the project root (or `src/`):
```ts
export async function register() {
  if (process.env.NEXT_RUNTIME === "nodejs") {
    await import("./instrumentation.node");     // Node-only SDKs, keep them out of the edge bundle
  }
}
```
`register()` runs once when a server instance starts, before requests are handled. Ran on 16.4.2: with only Node routes it logged once (`NEXT_RUNTIME=nodejs`); with a `middleware.ts` present it also ran with `NEXT_RUNTIME=edge`, so guard runtime-specific code.

## 2. OpenTelemetry quick start
```ts
// instrumentation.ts
import { registerOTel } from "@vercel/otel";
export function register() { registerOTel({ serviceName: "shop-web" }); }
```
`registerOTel` accepts a service-name string or a config object (checked in the `@vercel/otel` type definitions). Exporter config via the standard OpenTelemetry env vars such as `OTEL_EXPORTER_OTLP_ENDPOINT` (see the OTel exporter specification). For full control use `@opentelemetry/sdk-node` with `NodeSDK`, resources and exporters in `instrumentation.node.ts`.

Next emits spans out of the box for the incoming request, route rendering, `fetch`, route handlers and metadata resolution (span types such as `BaseServer.handleRequest`, `AppRender.fetch`, `ResolveMetadata.generateMetadata` in `next/dist/server/lib/trace/constants.js`; display names vary by version, so read them from your trace backend). `NEXT_OTEL_VERBOSE=1` makes the tracer emit all spans, not only that allowlist (checked in the tracer source). Wrap your own work:
```ts
import { trace } from "@opentelemetry/api";
await trace.getTracer("shop").startActiveSpan("checkout.price", async (span) => { try { ... } finally { span.end(); } });
```

## 3. onRequestError (Next 15+)
```ts
export async function onRequestError(err, request, context) {
  await fetch(process.env.ERROR_WEBHOOK!, {
    method: "POST",
    body: JSON.stringify({ message: err.message, digest: err.digest, path: request.path,
                           routeType: context.routeType, routePath: context.routePath }),
  });
}
```
Ran on 16.4.2: a server component that threw produced `message`, `digest` (the same digest the browser shows), `path`, `method`, `routeType: "render"`, `routePath`, `routerKind: "App Router"` and `renderSource: "react-server-components"`. The docs say it also covers route handlers, server actions and proxy.

## 4. Client side
`instrumentation-client.ts` (introduced in v15.3 per the docs version history) runs before the app hydrates - initialise RUM/analytics/error SDKs there. Report Web Vitals with `useReportWebVitals`.

## 5. Gotchas
- Heavy imports at the top of `instrumentation.ts` load in every runtime; use dynamic imports by `NEXT_RUNTIME`.
- Check that trace context reaches outgoing requests made by custom HTTP clients.
- Sample in production: `OTEL_TRACES_SAMPLER=parentbased_traceidratio` with `OTEL_TRACES_SAMPLER_ARG=0.1` (a probability in 0..1, per the OpenTelemetry SDK environment-variable spec).

## Verify
- [ ] Traces appear in the backend (Jaeger/Honeycomb/Datadog) with route names.
- [ ] Throwing in a server component triggers `onRequestError` with the digest shown to the user.
- [ ] Edge routes still build (no Node-only imports leaked).

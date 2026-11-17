---
id: computing-software.web-development.sveltekit.sveltekit-opentelemetry-tracing
name: sveltekit-opentelemetry-tracing
category: computing-software
field: web-development
product: sveltekit
tags: [sveltekit, observability, opentelemetry, tracing, instrumentation, jaeger, ssr-external]
level: advanced
status: docs-checked
description: "Enable SvelteKit server-side OpenTelemetry spans, set up instrumentation.server.js with Jaeger locally, and fix auto-instrumentation broken by bundling."
sources:
  - https://github.com/sveltejs/kit/blob/main/documentation/docs/30-advanced/68-observability.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SvelteKit observability (OpenTelemetry)

Available since 2.31. SvelteKit can emit server-side spans for `handle` (and `sequence` children), server and universal `load` (when run on the server), form actions, `+server` handlers, and remote functions. You must also collect them somewhere.

## Enable

In `vite.config.js`:

```js
sveltekit({
	tracing: {
		server: true
	}
})
```

Tracing has non-trivial overhead; consider enabling it only in development and preview.

Put your tracing setup in `src/instrumentation.server.ts` (or `.js`). It is loaded before application code, provided your platform supports it and your adapter is aware of it.

## Annotate spans

`event.tracing.root` is the span for the root `handle`; `event.tracing.current` is the span of the active handle/load/action/handler/remote function.

```js
import { getRequestEvent } from '$app/server';

async function authenticate() {
	const user = await getAuthenticatedUser();
	const event = getRequestEvent();
	event.tracing.root.setAttribute('userId', user.id);
}
```

## Local quickstart with Jaeger

Run a Jaeger collector, enable tracing, then install:

```sh
npm i @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node @opentelemetry/exporter-trace-otlp-proto import-in-the-middle
```

`src/instrumentation.server.js`:

```js
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto';
import { register } from 'import-in-the-middle/register-hooks.mjs';

register();

const sdk = new NodeSDK({
	serviceName: 'test-sveltekit-tracing',
	traceExporter: new OTLPTraceExporter(),
	instrumentations: [getNodeAutoInstrumentations()]
});

sdk.start();
```

Traces then appear in Jaeger's console at localhost:16686. The synchronous `register()` needs Node.js 22.22.3+, 24.11.1+, 25.1.0+ or 26.0.0+ and throws on older versions; the docs give a fallback using `supportsSyncHooks()` and `createAddHookMessageChannel()` with `node:module` register.

## `@opentelemetry/api`

It is an optional peer dependency. If SvelteKit reports it cannot find it, you likely have not set up collection yet (SDK packages bring it in); otherwise install it yourself.

## Bundling caveats

Interceptors must be installed before the instrumented module is evaluated. Bundling can break this by sharing chunks between instrumentation and app code, or by inlining the library. SvelteKit externalizes `@opentelemetry/api` itself. For another library, externalize it:

```js
export default defineConfig({
	plugins: [sveltekit()],
	ssr: { external: ['my-database-library'] }
});
```

Do not externalize application source files or dependencies indiscriminately. Runtime dependencies must be in `dependencies`, not `devDependencies`; `adapter-node` keeps `dependencies` external from its bundle, but other official adapters do not apply that rule, so check your adapter/platform. Also, importing `$app/env/*` evaluates `src/env.js` first, so anything it imports cannot be instrumented.

## Checked

Checked 2026-11-07.

Method: documentation only; no commands were run.

Read 30-advanced/68-observability.md in full: spans list, tracing.server, event.tracing, Jaeger setup, Node version floors, the sync-hooks fallback, ssr.external and the adapter-node dependency rule. No claims trimmed.

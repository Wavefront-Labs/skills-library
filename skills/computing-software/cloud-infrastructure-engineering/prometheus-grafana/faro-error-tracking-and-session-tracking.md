---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.faro-error-tracking-and-session-tracking
name: faro-error-tracking-and-session-tracking
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [faro, faro-error-tracking, faro-sessions, frontend-observability, real-user-monitoring, source-maps]
level: advanced
status: docs-checked
description: "Grafana Faro Web SDK error and session tracking: pushError, ignoreErrors, preserveOriginalError, session options and timeouts, console capture, private source map uploads."
sources: ["https://grafana.com/docs/grafana-cloud/monitor-applications/frontend-observability/instrument/error-tracking/", "https://grafana.com/docs/grafana-cloud/monitor-applications/frontend-observability/instrument/session-tracking/", "https://grafana.com/docs/grafana-cloud/monitor-applications/frontend-observability/instrument/console-instrumentation/", "https://grafana.com/docs/grafana-cloud/monitor-applications/frontend-observability/sourcemap-upload-plugins/", "https://github.com/grafana/faro-web-sdk"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Faro error tracking and sessions

**Goal:** see real users' browser errors with readable stack traces and group signals by session. The Faro Web SDK instruments pages running in a browser; browser extensions, web workers, Node.js and server runtimes are not supported.

## Initialise
Error, session and console instrumentation are enabled by default with a minimal setup (the docs use a placeholder collector URL of the form `https://my-domain.my-tld/collect/{app-key}`; use the URL from your Frontend Observability app):
```ts
initializeFaro({
  url: 'https://my-domain.my-tld/collect/{app-key}',
  app: { name: 'my-app' },
});
```
If you overwrite the `instrumentations` array you must include them yourself, for example `instrumentations: [...getWebInstrumentations()]`. `getWebInstrumentations({ captureConsole: false })` turns console capture off.

## Errors
- The error instrumentation hooks `window.onerror` and `onunhandledrejection` and reports through `faro.api.pushError()`; it should normally stay enabled because it is the only way errors are captured automatically. Faro errors are stored as logs identified by the `kind=error` label.
- Manual: `faro.api.pushError(error, { type: 'network', context: {...} })`. Options: `stackFrames`, `type`, `context`, `skipDedupe` (push even if identical to the previous one), `spanContext`, `timestampOverwriteMs`.
- Exclude errors with `ignoreErrors: ['My Error', /.*other-error.*/]` (strings or regular expressions).
- Third-party script errors appear as a generic "script error"; to get details add `crossorigin="anonymous"` to the script tag and have the server send `Access-Control-Allow-Origin`.
- Odd throws (`throw undefined`, `throw ''`): set `preserveOriginalError: true` and read `payload.originalError` in `beforeSend`, which can mutate or drop items before they are sent. Faro removes the original error before sending.

## Source maps
Frontend Observability uses source maps to deobfuscate minified stack traces. The docs say not to host source maps publicly (users could reconstruct your code) and to upload them privately to Grafana Cloud using the Faro bundler plugins (Webpack, Rollup/Vite), the Faro CLI or cURL. Prerequisites: app instrumented with the Faro Web SDK, telemetry reaching a Faro collector in Grafana Cloud, and an API key. The plugins support client-side rendered applications only, not server-side rendering.

## Sessions
- Option defaults: `enabled` false for session management in the option table (the instrumentation is on by default with no config), `persistent` false, `samplingRate` 1, `maxSessionPersistenceTime` 15 minutes plus a 1 minute buffer (tracked sessions only). Other options: `onSessionChange(oldSession, newSession)`, `sampler`, `generateSessionId`, `session`.
- A session ends after a maximum lifetime of 4 hours or 15 minutes of inactivity; the SDK then creates a new one (adding `previousSession`).
- Modes: `persistent: true` uses Local Storage (survives reloads, syncs across tabs of one browser; users sharing a browser can share a session id, so shorten `maxSessionPersistenceTime` or call `PersistentSessionsManager.removeUserSession()`); volatile (default) uses Session Storage, where a new tab gets a new session.
- Lifecycle events: `session_start`, `session_resume`, `session_extend`. Faro sends an `x-faro-session-id` header to the collector.
- `samplingRate` ranges 0 to 1 (fraction of signals sent); sampling is described on a separate page that was not read.
- `faro.api.setSession()` replaces the session meta (merge attributes yourself via `getSession()`); keeping the same session id only updates attributes and emits no `session_extend` (SDK v1.13.0 or later). Session tracking needs SDK v1.3.6 or later.

## Console capture and cost
Console instrumentation sends `console.*` calls as logs; `console.debug`, `console.trace` and `console.log` are disabled by default. Enabling all levels raises data volume and cost. Configure with `consoleInstrumentation: { consoleErrorAsLog: true, captureConsoleDisabledLevels: [...] }`.

## Verify
- [ ] A test error thrown in a non-production build shows up in Frontend Observability with a deobfuscated stack once source maps are uploaded.
- [ ] Session events (`session_start`) appear and the session id stays the same across page reloads when `persistent: true`.

## Checked
Date: 2026-11-07. Read in full: the Grafana Cloud Error tracking, Session tracking and Console instrumentation pages, the Source map uploads page, the Frontend Observability landing, Instrument and Get started pages, and the faro-web-sdk GitHub README. The docs URLs now redirect to a `/observe-and-act/` path; the old URLs fetched live (HTTP 200). Corrections: the draft's `url` pointed at a `faro-collector-prod-eu-west-0.grafana.net` collect URL that returned 404, replaced with the docs' placeholder form; the draft's `persistent: true` description matches the docs, but `samplingRate`, `persistent` and `enabled` defaults are now taken from the option table. Removed as not on these pages: `app.version` / `environment` fields, `TracingInstrumentation` usage, `faro.api.setUser`, `faro.pause()` and consent advice, the "keyed by app name + bundle/version" source map rule, the Errors/Session view descriptions, and the `beforeSend` URL-masking advice (the page only says `beforeSend` can mutate or drop items). The per-bundler upload pages and the sampling page were not opened.
Method: documentation only; no commands were run.

---
id: computing-software.web-development.frontend-development.error-tracking-with-sentry
name: error-tracking-with-sentry
category: computing-software
field: web-development
product: frontend-development
tags: [sentry, error-tracking, source-maps-upload, pii-scrubbing, release-tracking, observability]
level: practitioner
status: docs-checked
description: "Front-end and Node error tracking with Sentry: init options, releases and source map upload (then hiding maps), PII scrubbing, noise filtering, replay masking and alerting."
sources:
  - https://docs.sentry.io/platforms/javascript/configuration/options/
  - https://docs.sentry.io/platforms/javascript/sourcemaps/
  - https://docs.sentry.io/platforms/javascript/data-management/sensitive-data/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error tracking with Sentry

## 1. Init
```js
import * as Sentry from "@sentry/browser";      // pick the package for your framework
Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  environment: import.meta.env.MODE,
  release: __APP_VERSION__,                      // must match the uploaded source maps' release
  sendDefaultPii: false,
  tracesSampleRate: 0.1,
  replaysOnErrorSampleRate: 0.5,                 // needs the replay integration: see Sentry's Session Replay docs for masking options
  ignoreErrors: [],                              // add known-noisy messages here
  denyUrls: [/extensions\//i, /^chrome-extension:\/\//i],
  beforeSend(event) { if (event.request?.cookies) delete event.request.cookies; return event; },
});
Sentry.setUser({ id: user.id });                 // id only, not email, unless you have a basis to send it
```

## 2. Source maps
Upload source maps to Sentry at build time using your bundler's Sentry plugin or the Sentry CLI (follow Sentry's source maps page for the current setup), keep the `release` value identical in `Sentry.init` and the upload, and do not serve the `.map` files publicly.

## 3. Privacy
- Keep `sendDefaultPii` off unless you have a basis to send personal data.
- Breadcrumbs can capture URLs: strip query tokens in `beforeBreadcrumb`.
- Replay: keep masking on; unmask only specific safe elements.
- Check Sentry's data-management docs for server-side scrubbing and data residency options.

## 4. Noise and cost
Merge duplicates with grouping rules, filter known-noisy errors with `ignoreErrors` and `denyUrls`, and use the `tunnel` option if ad blockers drop events.

## 5. Act on it
Alert on new issues in a release and on regressions; review top issues weekly.

## Verify
- [ ] A test error thrown in production shows a de-minified stack trace with original file names, and no cookies or tokens in the event payload.

## Checked
2026-10-28. Confirmed on the Sentry JavaScript options and sensitive-data pages: `sendDefaultPii`, `beforeBreadcrumb`, `tracesSampleRate`, `replaysOnErrorSampleRate`, `ignoreErrors`, `denyUrls`, `tunnel`. Removed: replay integration arguments, plugin and `filesToDeleteAfterUpload` options, `hidden` source maps, debug-ID and CLI explain claims, sensitive-field names, inbound filter and spike-protection claims, suspect commits (not located on fetched pages).
Method: documentation only; no commands were run.

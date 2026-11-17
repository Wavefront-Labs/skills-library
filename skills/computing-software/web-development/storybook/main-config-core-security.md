---
id: computing-software.web-development.storybook.main-config-core-security
name: main-config-core-security
category: computing-software
field: web-development
product: storybook
tags: [allowedhosts, core-config, security, insecureiframemessaging, telemetry]
level: advanced
status: docs-checked
description: "Configure core options such as allowedHosts, builder and telemetry, and the iframe security flags."
sources:
  - https://storybook.js.org/docs/api/main-config/main-config-core
  - https://storybook.js.org/docs/api/main-config/main-config-security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# core and security config

Goal: secure the dev server and tune internals.

`core` fields: `allowedHosts` (string array or `true`, default `[]`), `builder` (`@storybook/builder-vite` or `@storybook/builder-webpack5`, optionally with `options`), `channelOptions`, `crossOriginIsolated`, `disableProjectJson`, `disableTelemetry`, `disableWebpackDefaults`, `disableWhatsNewNotifications`, `enableCrashReports`, `renderer`.

```ts
core: {
  allowedHosts: ['storybook.internal.example'],
  disableTelemetry: true,
},
```

`allowedHosts` validates the `Host` header of requests (and the `Origin` of WebSocket connections) against the list; Storybook's localhost or `--host` address is always allowed. Use it behind a reverse proxy. `true` disables validation and is insecure. It protects against DNS rebinding but not against other machines on your network: anyone who can reach the dev server has the same access, and the server listens on localhost only unless you pass `--host`.

The docs prefer `framework.options.builder` for builder options and say to use `core.builder.options` only for a builder that is not part of a framework. `channelOptions.maxDepth` defaults to 3.

`security` (both default `false`):
- `insecureIframeMessaging`: turns off the origin checks on messages between manager and preview iframes and restores older behavior; use with caution.
- `insecureRemoteIframeEmbed`: lets the dev server's manager and preview be embedded in an iframe on any origin (by default only localhost and 127.0.0.1 pages); use with caution.

```ts
security: { insecureRemoteIframeEmbed: true },
```
For both, the docs' safer alternative is to build the composed Storybook and compose the build output.

Verify: a request with an unlisted host is rejected.

## Checked
Date: 2026-11-04. Read the core and security main-config pages (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: all field names, defaults, DNS rebinding and network-exposure wording, both security flags.
Fixed: dropped the claim that the remote embed flag is needed for composing a remote dev Storybook; the pages recommend composing a build. Added the builder-options preference and `maxDepth` default.
Conflict: builder options are shown under `core.builder.options` here and in the Vite builder page, while the core page says `framework.options.builder` is preferred.
Method: documentation only; no commands were run.

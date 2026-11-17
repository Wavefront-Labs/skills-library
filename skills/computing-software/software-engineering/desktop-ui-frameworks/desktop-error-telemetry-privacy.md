---
id: computing-software.software-engineering.desktop-ui-frameworks.desktop-error-telemetry-privacy
name: desktop-error-telemetry-privacy
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [desktop-error-telemetry-privacy, desktop-crash-reporting, crash-reporting, minidump, sentry, desktop-ui-frameworks]
level: practitioner
status: draft
description: "Scrub personal data and obtain consent before sending reports."
sources:
  - https://docs.sentry.io/platforms/
  - https://chromium.googlesource.com/crashpad/crashpad/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Crash report privacy and consent

**Goal:** compliant diagnostics.

```text
Minimum fields: app version, OS, stack, anonymous install id
Scrub: user paths (<USER_HOME>), email, tokens in breadcrumbs; beforeSend hooks (Sentry) / custom filters
Consent: opt-in on first run or setting; document retention and region
Rate limit and dedupe by stack hash to avoid flooding
```

**Gotcha:** Minidumps contain process memory and can hold secrets; treat them as sensitive and restrict access.

## Verify
- A sample report contains no usernames or file paths.

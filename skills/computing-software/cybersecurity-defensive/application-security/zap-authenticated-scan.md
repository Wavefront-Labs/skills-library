---
id: computing-software.cybersecurity-defensive.application-security.zap-authenticated-scan
name: zap-authenticated-scan
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [zap-authenticated-scan, owasp-zap, dast, automation-framework, browser-based-authentication, session-management]
level: practitioner
status: docs-checked
description: "Set up authenticated ZAP scans in the Automation Framework environment: context URLs, authentication method, verification, session management, users and TOTP."
sources: ["https://www.zaproxy.org/docs/desktop/addons/automation-framework/environment/", "https://www.zaproxy.org/docs/desktop/addons/automation-framework/", "https://www.zaproxy.org/docs/desktop/addons/authentication-helper/browser-auth/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ZAP authenticated scans

Unauthenticated DAST only sees what is reachable without logging in. ZAP needs a context with a user and a
reliable way to log in and stay logged in. The Automation Framework supports all of ZAP's authentication
mechanisms.

## Environment section (Automation Framework)
Under `env: contexts:` each context has:
- `name`, `urls` (everything under each URL is included), optional `includePaths` and `excludePaths` regexes.
- `authentication.method`: one of `manual`, `http`, `form`, `json`, `script`, `autodetect`, `browser`, `client`.
  `form`/`json` take `loginPageUrl`, `loginRequestUrl`, `loginRequestBody`; `http` takes `hostname`, `port`,
  `realm`; `script` takes `script` or `scriptInline` plus `scriptEngine`.
- `authentication.verification.method`: one of `response`, `request`, `both`, `poll`, with `loggedInRegex` /
  `loggedOutRegex`; for `poll` also `pollFrequency`, `pollUnits` (`requests` or `seconds`), `pollUrl`,
  `pollMethod`, `pollPostData`, `pollAdditionalHeaders`.
- `sessionManagement.method`: `cookie`, `http` or `script`.
- `users`: a list with `name` and `credentials` (`username`, `password`, vars supported; an optional `totp`
  block with `secret`, `period` default 30, `digits` default 6, `algorithm` default SHA1, supported by Browser
  Based Authentication).
- `env.vars` define custom variables usable as `${name}`.

Jobs then refer to the context and user by name. Job pages exist for spider, passiveScan-wait, activeScan and
others; read each job's page for its parameters before writing the plan.

## Tips
- When the target uses a default port (80 or 443), leave the port out of the context URL: including it can
  stop ZAP crawling or testing the target.
- Keep a verification method configured so a lost session is noticed.
- Exclude logout and other destructive URLs via `excludePaths`; scan a test tenant, staging only unless agreed.
- The desktop UI has an Authentication Tester dialog for debugging a setup before automating.

## Verify
Run a short scan and confirm authenticated-only URLs appear in the report; the Authentication Helper add-on
documents an authentication report for diagnostics.

## Checked
2026-11-01. Confirmed against the ZAP Automation Framework Environment page (all keys and enums above, port
note, TOTP defaults) and the desktop help index (Authentication Tester dialog, job pages). Removed: the full
example plan, `loginPageWait`/`browserId`, the `spiderAjax` and report job parameters, the Docker command,
`ZAP_AUTH_HEADER_VALUE`, and CAPTCHA/CSRF/MFA advice.
Method: documentation only; no commands were run.

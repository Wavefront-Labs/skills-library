---
id: computing-software.cybersecurity-defensive.application-security.content-security-policy-rollout
name: content-security-policy-rollout
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [security-headers, content-security-policy, csp, nonce, strict-dynamic, report-only, xss-mitigation, trusted-types]
level: advanced
status: docs-checked
description: "Roll out a strict nonce-based Content Security Policy: start in report-only, collect violations, remove inline script, then enforce with strict-dynamic."
sources: ["https://web.dev/articles/strict-csp", "https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Content Security Policy roll-out

**Goal:** an enforced CSP that blocks injected script, without breaking the site.

## Target policy (strict, nonce-based)
```
Content-Security-Policy:
  script-src 'nonce-{RANDOM}' 'strict-dynamic' https: 'unsafe-inline';
  object-src 'none';
  base-uri 'none';
  frame-ancestors 'self';
  report-to csp-endpoint
```
- A fresh cryptographically random nonce per response (>=128 bits, base64) on every `<script nonce=...>`.
- `'strict-dynamic'` lets nonce'd scripts load further scripts; modern browsers then ignore `https:` and
  `'unsafe-inline'`, which remain only as fallbacks for old browsers.
- Allow-list policies (`script-src cdn.example.com`) are routinely bypassable via JSONP/AngularJS on allowed hosts; prefer nonces or hashes.

## Procedure
1. Deploy as `Content-Security-Policy-Report-Only` with a `Reporting-Endpoints: csp-endpoint="https://.../csp"` header (plus legacy `report-uri`).
2. Collect and group violations by `blocked-uri` and `effective-directive`.
3. Refactor: move inline `<script>` blocks into nonce'd tags, replace `onclick=` handlers and `javascript:` URLs with `addEventListener`, remove `eval`/`new Function` (or accept `'unsafe-eval'` knowingly).
4. Add the nonce in the templating layer (middleware generates it, templates read it). Do not cache HTML with a fixed nonce at the CDN.
5. Enforce. Keep report-only for a tighter next version in parallel.

## Gotchas
- Static nonce or nonce reused across responses defeats the policy.
- Third-party tag managers inject inline scripts; they need nonce propagation support.

## Verify
- [ ] Google CSP Evaluator rates the policy without high-severity findings.
- [ ] Injecting `<script>alert(1)</script>` through a test reflected parameter is blocked (console shows violation).
- [ ] Violation report volume is near zero for a week before enforcing.

## Checked
2026-10-28. Confirmed against official pages: nonce plus strict-dynamic policy with object-src none and base-uri none (web.dev strict CSP), 128-bit nonce, allow-list bypass via JSONP/AngularJS and report-only rollout (OWASP CSP Cheat Sheet, web.dev), CSP Evaluator.
Removed or rewritten: Trusted Types step, the meta-tag limitation bullet and the multiple-header bullet (not in the fetched pages); non-URL sources replaced with fetched pages.
Method: documentation only; no commands were run.

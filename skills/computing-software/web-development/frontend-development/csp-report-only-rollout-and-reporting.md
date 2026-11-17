---
id: computing-software.web-development.frontend-development.csp-report-only-rollout-and-reporting
name: csp-report-only-rollout-and-reporting
category: computing-software
field: web-development
product: frontend-development
tags: [content-security-policy, csp, csp-report-only, csp-reporting, report-to, reporting-api, csp-violations, report-uri]
level: practitioner
status: docs-checked
description: "Rolling out CSP safely with Report-Only, collecting violations via report-to/report-uri, filtering extension noise and moving to enforcement."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy-Report-Only
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/report-to
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/report-uri
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Reporting-Endpoints
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSP Report-Only rollout and reporting

**Goal:** turn on CSP without breaking production, using real violation data to fix the site first.

## 1. Two headers side by side
```
Content-Security-Policy: object-src 'none'; base-uri 'none'            (enforced, safe subset)
Content-Security-Policy-Report-Only: script-src 'nonce-…' 'strict-dynamic'; report-to csp; report-uri /csp-report
Reporting-Endpoints: csp="https://example.com/csp-report"
```
Report-Only never blocks; it only reports, and it cannot be delivered in a `<meta>` element. Send both `report-to` (named by the `Reporting-Endpoints` header) and the deprecated `report-uri`: browsers that support `report-to` ignore `report-uri`, and `report-to` support in CSP is recent in Firefox (149 per MDN browser-compat data; Chrome 70, Safari 16.4).

## 2. Collector
- `report-uri` posts `Content-Type: application/csp-report` with `{"csp-report": {...}}`.
- Reporting API posts `application/reports+json`: reports with `type: "csp-violation"` and a `body` containing fields such as `blockedURL`, `effectiveDirective`, `sourceFile`, `lineNumber`, `sample`, `disposition` and `originalPolicy`.
Configure the collector's body parser to accept both content types, rate-limit the endpoint, store fields rather than raw bodies, and don't require auth or CSRF tokens on it.

## 3. Triage
Group by `effectiveDirective` + `blockedURL` origin. Ignore noise caused by browser extensions (browser-injected scripts and styles). Fix: missing nonces, inline handlers, third-party tags that need `strict-dynamic`.

## 4. Promotion
1. Report-Only for ~1-2 weeks covering all page types and logged-in states.
2. When remaining reports are noise, switch the same policy to the enforcing header and **keep** reporting (`report-to`) to catch regressions.
3. Tighten in steps (`style-src`, `connect-src`) using another Report-Only header alongside the enforced one.

## Verify
- [ ] Collector receives reports from Chrome and Firefox (trigger a violation deliberately).
- [ ] Dashboard of violations by directive trends to near zero before enforcement.
- [ ] After enforcement, an alert fires on spikes.

## Checked
Checked 2026-10-26 against MDN (Content-Security-Policy-Report-Only, report-to, report-uri, Reporting-Endpoints) and MDN browser-compat-data (CSP report-to: Chrome 70, Firefox 149, Safari 16.4; report-uri deprecated). Confirmed: report-uri posts application/csp-report with a csp-report object; report-to posts application/reports+json with type csp-violation and the listed body fields; report-only is not allowed in meta; report-uri is ignored where report-to is supported. Corrected the stale claim that Firefox and Safari only support report-uri. Removed unconfirmed extension scheme names, the Express snippet and the 'batched and delayed' remark.

Method: documentation only; no commands were run.

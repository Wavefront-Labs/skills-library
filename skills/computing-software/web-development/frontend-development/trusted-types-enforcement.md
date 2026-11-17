---
id: computing-software.web-development.frontend-development.trusted-types-enforcement
name: trusted-types-enforcement
category: computing-software
field: web-development
product: frontend-development
tags: [xss, trusted-types, csp, dom-xss, security]
level: practitioner
status: docs-checked
description: "Enforcing Trusted Types with CSP to lock down DOM XSS sinks: report-only rollout, policies, default policy migration, and framework and library compatibility."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/trusted-types
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/require-trusted-types-for
  - https://developer.mozilla.org/en-US/docs/Web/API/TrustedTypePolicyFactory/createPolicy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trusted Types

Trusted Types makes injection sinks (`innerHTML`, `script.src`, `eval`, ...) reject plain strings; only objects created by a reviewed policy are accepted. It turns DOM XSS from "find every sink" into "review a few policies".

## 1. Roll out report-only
```
Content-Security-Policy-Report-Only: require-trusted-types-for 'script'; trusted-types app-html dompurify; report-to csp
```
Collect violations (sink + sample) for a few weeks; each one is a place that assigns strings to a sink.

## 2. Fix violations
- Prefer removing the sink: `textContent`, DOM APIs.
- Where HTML is needed, create a policy:
```js
const htmlPolicy = trustedTypes.createPolicy("app-html", {
  createHTML: s => DOMPurify.sanitize(s),
});
el.innerHTML = htmlPolicy.createHTML(userHtml);
```
- Script URLs: `createScriptURL: u => { const url = new URL(u, location.origin); if (url.origin !== location.origin) throw new TypeError("blocked"); return url.href; }`.
- Policy names must be listed in the `trusted-types` directive (valid names use alphanumerics and `-#=_/@.%`; `*` allows any); `'allow-duplicates'` permits creating a policy with a name that already exists, otherwise `createPolicy` throws a `TypeError`.

## 3. Default policy (migration aid)
```js
trustedTypes.createPolicy("default", { createHTML: (s, sink) => { report(sink); return DOMPurify.sanitize(s); } });
```
Per MDN, a policy named `default` is called for any string reaching a sink, so it is a migration aid for code you cannot change; keep it strict and logged, and refactor to explicit policies.

## 4. Enforce
Switch header to `Content-Security-Policy: require-trusted-types-for 'script'; trusted-types app-html dompurify default`.

## 5. Compatibility
- Per MDN browser-compat data: Chrome 83, Firefox 148, Safari 26 for the Trusted Types API and the `require-trusted-types-for` / `trusted-types` directives. Older browsers do not enforce the directive, so feature-detect `window.trustedTypes` before calling `createPolicy`.

## Verify
Under enforcement, passing a string to an injection sink throws a `TypeError` (MDN); tests that assign a string to `innerHTML` should fail.

## Checked
Checked 2026-10-26 against MDN Trusted Types API, the trusted-types and require-trusted-types-for directive pages, TrustedTypePolicyFactory.createPolicy (duplicate-name TypeError, default policy) and MDN browser-compat data (Chrome 83, Firefox 148, Safari 26). Removed unconfirmed items: the 'Baseline 2026' label, the tinyfill one-liner, the framework support list (Angular, Lit, React, webpack, Closure), the exact Chrome console message text and the DOMPurify RETURN_TRUSTED_TYPE option.

Method: documentation only; no commands were run.

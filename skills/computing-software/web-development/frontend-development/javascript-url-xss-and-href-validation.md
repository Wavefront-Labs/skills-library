---
id: computing-software.web-development.frontend-development.javascript-url-xss-and-href-validation
name: javascript-url-xss-and-href-validation
category: computing-software
field: web-development
product: frontend-development
tags: [javascript-url-scheme, href-sanitization, url-allowlist, xss, url-attributes, security]
level: practitioner
status: docs-checked
description: "Preventing XSS through URL attributes: javascript: and data: schemes in href/src/action, parsing with new URL and a protocol allowlist, framework behaviour and redirects."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html#safe-sinks
  - https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Schemes/javascript
  - https://react.dev/blog/2024/04/25/react-19-upgrade-guide
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# javascript: URLs and href validation

HTML escaping does not help here: `<a href="javascript:alert(document.cookie)">` contains no special characters to escape.

## 1. Dangerous sinks
`a[href]`, `area[href]`, `iframe[src]`, `form[action]`, `button[formaction]`, `object[data]`, `embed[src]`, `location.href = x`, `location.assign(x)`, `window.open(x)`, and server redirects to user-supplied URLs.

## 2. Validate by parsing, then allowlist
```js
const SAFE = new Set(["http:", "https:", "mailto:", "tel:"]);
export function safeHref(input, base = location.origin) {
  try {
    const u = new URL(String(input).trim(), base);
    return SAFE.has(u.protocol) ? u.href : "about:blank";
  } catch { return "about:blank"; }
}
```
Parse with the URL parser rather than a regex, and test odd forms (mixed case, leading whitespace, control characters inside the scheme). Never blocklist `javascript:` with a regex.
Avoid `data:` URLs from user input; if needed, allow only image types for `img`.

## 3. Framework behaviour
- Do not assume your framework blocks `javascript:` URLs in `href`/`src` props; check the version you ship and validate anyway (other schemes, `data:`, server rendering paths, `window.open`).
- Server templates escape HTML but not schemes; apply the same allowlist on the server.

## 4. Related
- Open redirects: validate redirect targets against an allowlist of hosts or allow only relative paths starting with a single `/` (reject `//evil.com` and `/\evil.com`).
- Add `rel="noopener noreferrer"` to user links opened in new tabs.
- A content security policy can block `javascript:` navigation (MDN notes `script-src` applies) as a backstop.

## Verify
- [ ] Unit tests: `javascript:alert(1)`, ` JAVASCRIPT:alert(1)`, `java\nscript:alert(1)`, `data:text/html,<script>`, `//evil.com` all yield a safe result.

## Checked
2026-10-28. Confirmed on MDN javascript: URLs: usable as navigation targets in href, form action, iframe src and window.location; discouraged; can be blocked by CSP `script-src`. OWASP XSS prevention cheat sheet cited for URL sinks. Removed: React 19/16.9-18 behaviour, Vue/Svelte/Angular claims, Rails specifics, scheme-normalisation list, `rel=ugc nofollow` (not confirmed).
Method: documentation only; no commands were run.

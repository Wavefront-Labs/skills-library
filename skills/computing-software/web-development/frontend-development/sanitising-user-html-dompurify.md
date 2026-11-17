---
id: computing-software.web-development.frontend-development.sanitising-user-html-dompurify
name: sanitising-user-html-dompurify
category: computing-software
field: web-development
product: frontend-development
tags: [xss, dompurify, html-sanitization, sanitizer-api, rich-text, security, markdown-sanitization]
level: practitioner
status: verified
description: "Allowing user-supplied HTML safely: DOMPurify configuration, allowlisting tags and attributes, link hardening, server-side sanitising, and the Sanitizer API."
sources:
  - https://github.com/cure53/DOMPurify
  - https://developer.mozilla.org/en-US/docs/Web/API/HTML_Sanitizer_API
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html#html-sanitization
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Sanitising user HTML

Escape by default. Sanitise only when users must author markup (rich-text editors, Markdown rendering, pasted HTML, email bodies).

## 1. DOMPurify in the browser
```js
import DOMPurify from "dompurify";
const clean = DOMPurify.sanitize(dirty, {
  ALLOWED_TAGS: ["p", "br", "strong", "em", "a", "ul", "ol", "li", "blockquote", "code", "pre", "h2", "h3"],
  ALLOWED_ATTR: ["href", "title"],
  ALLOW_DATA_ATTR: false,
});
DOMPurify.addHook("afterSanitizeAttributes", node => {
  if (node.tagName === "A") { node.setAttribute("rel", "noopener noreferrer nofollow"); node.setAttribute("target", "_blank"); }
});
el.innerHTML = clean;
```
- Default config already strips scripts, event handlers and `javascript:` URLs, but (tested in DOMPurify 3.4 + jsdom) it keeps `style` and `data-*` attributes, `<img src>`, `<svg>` and `<math>`; an explicit allowlist like the one above removes them. The hook runs after attribute sanitising, so the `rel`/`target` it adds survive.
- Sanitise immediately before insertion, and **do not modify the string afterwards** (string manipulation after sanitising can reintroduce markup - mutation XSS).
- With Trusted Types: `DOMPurify.sanitize(x, { RETURN_TRUSTED_TYPE: true })` (documented in the DOMPurify README; it returns a plain string where `trustedTypes` does not exist, e.g. jsdom, so test it in a real browser).
- In Node, `createDOMPurify(new JSDOM("").window)` is the setup.

## 2. Server side
Sanitise on output or on save (store original + sanitised). Node: DOMPurify + `jsdom`, or `sanitize-html`. Python: `nh3` (`nh3.clean` dropped `onclick`, `<script>` and the `javascript:` href in a test; bleach was declared deprecated in January 2023 and is "Development Status :: 7 - Inactive" on PyPI). Ruby: `Rails::HTML5::SafeListSanitizer` / `sanitize` helper. Java: OWASP Java HTML Sanitizer. Keep the library updated - bypasses are found and patched regularly.

## 3. Markdown
Markdown allows raw HTML by default. Render then sanitise (`marked` -> DOMPurify), or disable HTML (`markdown-it` `html: false`). In a test `marked.parse` passed `<img onerror>` and a `javascript:` link straight through, while `markdown-it` with `html: false` escaped the tag and refused to link `javascript:`; with `html: true` the raw tag passes. Always check link schemes.

## 4. Sanitizer API
`el.setHTML(dirty)` sanitises with a safe default and cannot produce script execution; custom `Sanitizer` configs refine it. MDN compat data lists `Element.setHTML` from Chrome 146 and Firefox 148, not in Safari; feature-detect and fall back to DOMPurify.

## 5. Do not
- Write regex-based sanitisers.
- Allow `style` attributes (CSS-based data exfiltration, UI redressing) or `<svg>`/`<math>` unless needed.
- Sanitise then insert into a different context (attribute, URL) than HTML body.

## Verify
Run payload lists (PortSwigger XSS cheat sheet, mXSS cases) through your exact config in a unit test; CSP report-only shows no inline-script violations from user content.

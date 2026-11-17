---
id: computing-software.web-development.node-express.context-aware-output-encoding
name: context-aware-output-encoding
category: computing-software
field: web-development
product: node-express
tags: [xss, output-encoding, auto-escaping, template-engines, owasp, security, json-script-embedding]
level: practitioner
status: gated
description: "Preventing XSS with context-aware output encoding: HTML body vs attribute vs JS vs URL vs CSS contexts, auto-escaping template engines, and the contexts escaping cannot save."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
  - https://owasp.org/Top10/A03_2021-Injection/
  - https://expressjs.com/en/guide/using-template-engines.html
  - https://mozilla.github.io/nunjucks/api.html#autoescaping
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Context-aware output encoding

**Rule:** encode untrusted data at output time, for the exact context it lands in. Input filtering is not a substitute.

## 1. Contexts
| Context | Example | Encoding |
|---|---|---|
| HTML body | `<p>{{name}}</p>` | HTML entity: `& < > " '` |
| Quoted attribute | `<input value="{{q}}">` | HTML attribute encoding; **always quote** attributes |
| URL parameter | `<a href="/s?q={{q}}">` | `encodeURIComponent`, then HTML-attribute encode |
| Whole URL in href/src | `<a href="{{url}}">` | validate scheme allowlist (`https:`, `mailto:`) - encoding does not stop `javascript:` |
| JavaScript data | `<script>const d = {{json}}</script>` | serialise JSON and escape `<` as `\u003c` (or put data in `<script type="application/json">` / a data attribute and parse) |
| CSS | `style="color: {{c}}"` | strict allowlist only |
| Event handler / unquoted attr / `<script>` body / template literal | `onclick="{{x}}"` | **never place untrusted data here** |

## 2. Auto-escaping engines
Escape by default for HTML body/attribute (all ran this session with the input `<b>"'&`): React JSX (react-dom/server), Vue templates (@vue/server-renderer), Django templates, Handlebars `{{ }}`, EJS `<%= %>`, Pug `#{}` and Nunjucks (3.x escaped by default in a plain `new Environment()`; still set `autoescape: true` explicitly). Plain `jinja2.Template` does NOT escape (ran: output unchanged); Jinja2 needs `autoescape=True` or `select_autoescape()` (Flask enables it for `.html`). Pug text interpolation escapes `& < > "` but left `'` as is, so keep attributes double-quoted. Angular, Svelte and Rails ERB are documented to escape by default (gated: unconfirmed, source is paywalled or blocked).
Unescaped forms to grep for in review: EJS `<%-`, Handlebars `{{{ }}}`, Pug `!{}`, Nunjucks/Jinja/Django `| safe`, Django `mark_safe`/`{% autoescape off %}`, Rails `raw`/`html_safe`, React `dangerouslySetInnerHTML`, Vue `v-html` (all except Rails and `mark_safe` ran and emitted the raw input).

## 3. Embedding server data for the client
```js
// Express + EJS
res.render("page", { boot: JSON.stringify(data).replace(/</g, "\\u003c") });
// template: <script id="boot" type="application/json"><%- boot %></script>
// client: JSON.parse(document.getElementById("boot").textContent)
```
Without escaping `<`, a value containing `</script><script>alert(1)</script>` breaks out (ran with EJS: unescaped JSON produced extra `<script>` tags; the `<` version produced one tag and `JSON.parse` returned the original string).

## 4. Other outputs
- JSON APIs: send `Content-Type: application/json` and `X-Content-Type-Options: nosniff`; never reflect input into `text/html` error pages.
- Emails, PDFs, SVG generation, CSV (formula injection: prefix `= + - @` cells with `'`) have their own contexts.

## Verify
- Test inputs per field: `"><svg onload=alert(1)>`, `'-alert(1)-'`, `javascript:alert(1)`, `</script><script>alert(1)</script>`.
- Semgrep rules for unescaped template syntax in CI; a CSP as defence in depth.

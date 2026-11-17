---
id: computing-software.web-development.frontend-development.html-validation-nu-checker
name: html-validation-nu-checker
category: computing-software
field: web-development
product: frontend-development
tags: [nu-html-checker, html-validator, vnu, html-conformance, html-parse-errors, html]
level: practitioner
status: docs-checked
description: "Validating HTML with the Nu Html Checker (web, vnu.jar, CI), reading its errors and fixing the parse errors that break accessibility and layout."
sources:
  - https://validator.github.io/validator/
  - https://validator.w3.org/nu/
  - https://html.spec.whatwg.org/multipage/parsing.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTML validation with the Nu checker

## 1. Run it
- Web: validator.w3.org/nu (URL, upload, or paste; "Show source" highlights).
- Local / CI (vnu.jar needs Java 17 or above; the pre-compiled binaries need no Java):
```bash
npm i -D vnu-jar
java -jar node_modules/vnu-jar/build/dist/vnu.jar --skip-non-html dist/
# see `vnu.jar --help` for output format, error-only and message-filter options
```
- Validate the **rendered** HTML for SPAs/SSR: save the rendered HTML from your test browser and validate that file.

## 2. Errors that actually matter
| Error class | Why it matters | Fix |
|---|---|---|
| Duplicate id | breaks `label for`, `aria-labelledby`, skip links | unique ids (React `useId`) |
| Block element inside `button` / `p` | parser closes `<p>` early; layout differs from source | use `span`, restructure |
| Stray end tag (typical) | earlier element already closed implicitly | find the auto-closed parent |
| Attribute not allowed on element | ARIA misuse e.g. `aria-label` on `div` with no role | add role or use real element |
| Bad `href` value (spaces) | broken links | URL-encode |
| `for` not pointing at a labelable control | label not associated | point at the input id |
| `li` outside `ul`/`ol` | list semantics lost | wrap in `ul`/`ol` |

## 3. How the parser rewrites invalid markup
The HTML parsing spec defines error recovery such as "foster parenting": content that is not allowed inside a `table` is moved before the table. Invalid nesting such as block elements inside `p` is recovered differently from what the source suggests. These are why "works in source, broken in DOM" bugs happen; compare DevTools Elements against source.

## 4. Noise you can ignore
Info-level and warning messages are advisory; triage errors first. Prefer `data-*` for custom attributes.

## Verify
- [ ] CI job fails on error-level messages from the validator.
- [ ] Zero duplicate-id errors on templates that render lists.

## Checked
2026-10-28. Confirmed on validator.github.io/validator: Java 17 or above for vnu.jar, `--skip-non-html`, npm package vnu-jar; WHATWG parsing page: foster parenting; React docs: `useId`. Removed: `--errors-only`, `--format`, `--filterpattern`, exact vnu message strings, Playwright call, specific parser rewrite outputs (not on the fetched pages).
Method: documentation only; no commands were run.

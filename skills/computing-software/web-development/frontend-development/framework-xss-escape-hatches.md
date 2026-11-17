---
id: computing-software.web-development.frontend-development.framework-xss-escape-hatches
name: framework-xss-escape-hatches
category: computing-software
field: web-development
product: frontend-development
tags: [xss, dangerouslysetinnerhtml, v-html, mark-safe, html-safe, security]
level: practitioner
status: docs-checked
description: "Auditing framework escape hatches that bypass auto-escaping: dangerouslySetInnerHTML, v-html, mark_safe, html_safe/raw, Svelte @html, and URL props, with safe patterns."
sources:
  - https://react.dev/reference/react-dom/components/common#dangerously-setting-the-inner-html
  - https://vuejs.org/guide/best-practices/security.html
  - https://docs.djangoproject.com/en/stable/ref/utils/#django.utils.safestring.mark_safe
  - https://guides.rubyonrails.org/security.html#cross-site-scripting-xss
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Framework escape hatches

Frameworks escape text by default; every XSS in a modern app goes through an explicit opt-out. Inventory and review them.

## 1. The hatches
| Framework | Hatch | Grep |
|---|---|---|
| React | `dangerouslySetInnerHTML={{ __html: x }}` | `dangerouslySetInnerHTML` |
| Vue | `v-html="x"`, `innerHTML` render props | `v-html` |
| Svelte | `{@html x}` | `@html` |
| Django | `mark_safe(x)`, `|safe`, `{% autoescape off %}`, `format_html` misuse | `mark_safe\|\|safe\|autoescape off` |
| Rails | `html_safe`, `raw` | `html_safe\|raw(` |
| Jinja2/Flask | `Markup(x)`, `|safe` | `Markup(\||safe` |

## 2. Safe patterns
- React: sanitise the string before passing it to `dangerouslySetInnerHTML`, ideally in one wrapper component so there is a single reviewed call site; lint-ban the prop elsewhere.
- Vue: the security guide warns against `v-html` with untrusted content; sanitise first, or render text with `{{ }}`.
- Django: build HTML with `format_html("<b>{}</b>", user_value)` (escapes args) instead of `mark_safe(f"<b>{user_value}</b>")`.
- Rails: use the sanitize helpers (see the Rails security guide, XSS section); never call `html_safe` on user input.

## 3. Non-obvious bypasses
- URL props: `<a href={user.website}>` - a `javascript:` URL can execute. Validate the scheme (allow `https:`/`http:`).
- Server-side rendered JSON state embedded in a script tag - escape `<`.
- React `ref.current.innerHTML =` and third-party libraries rendering HTML strings (chart tooltips, markdown renderers that allow raw HTML).
- Vue templates compiled from user input are template injection (the Vue security guide says never to use non-trusted content as a component template).
- Spreading user-controlled objects as props can set `dangerouslySetInnerHTML` or `href`.

## Verify
Grep/lint shows every hatch passes through the sanitiser wrapper; review checklist item "new escape hatch?" in PR template; payload test through each rich-content field.

## Checked
2026-10-28. Confirmed: React `dangerouslySetInnerHTML` page, Vue security guide (`v-html`, template warning), Django `format_html`/`mark_safe`, Rails security guide XSS section. Removed: Angular bypassSecurityTrust row, ESLint rule names, directive names, Rails `safe_join`/`content_tag`/`<%==`, template-engine row, `rehype-raw`.
Method: documentation only; no commands were run.

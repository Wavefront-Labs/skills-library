---
id: computing-software.web-development.responsive-design.responsive-html-email
name: responsive-html-email
category: computing-software
field: web-development
product: responsive-design
tags: [html-email, responsive-email, mjml, email-dark-mode, outlook-conditional-comments, email-accessibility]
level: practitioner
status: gated
description: "Building HTML email that renders across Gmail, Apple Mail and Outlook: table layout, inline styles, fluid/hybrid technique, MSO conditionals, dark mode, MJML and testing."
sources:
  - https://www.caniemail.com/
  - https://documentation.mjml.io/
  - https://www.goodemailcode.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responsive HTML email

Email clients are not browsers: classic Outlook for Windows renders with Word, Gmail strips or rewrites CSS in places, and images are often blocked (client behaviour not run here (gated: unconfirmed, source is paywalled or blocked); check caniemail.com).

## 1. Structure
```html
<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width">
<meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark">
<style>@media (max-width: 600px) { .col { display: block !important; width: 100% !important; } }</style>
</head><body style="margin:0;padding:0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">
  <!--[if mso]><table role="presentation" width="600"><tr><td><![endif]-->
  <div style="max-width:600px;margin:0 auto;"> ... </div>
  <!--[if mso]></td></tr></table><![endif]-->
</td></tr></table>
</body></html>
```
- Layout with `role="presentation"` tables; ~600px max width, fluid below.
- Inline critical styles (MJML/Maizzle/juice do it); keep media queries in `<head>` as enhancement.
- Hybrid ("spongy") columns: `display:inline-block; max-width:300px; width:100%` stack without media queries (run in Chromium: two such columns stacked at 280px and 400px and sat side by side at 700px); MSO conditionals give Outlook fixed tables (gated: unconfirmed, source is paywalled or blocked).

## 2. Tooling
- **MJML**: `npx mjml welcome.mjml -o welcome.html` compiles semantic components to bulletproof tables (run with mjml 5.4.1: a one-section file produced 4.8 KB of table markup with `role="presentation"` tables, `<!--[if mso | IE]>` conditionals and an `@media only screen and (min-width:480px)` rule).
- React Email / Maizzle (Tailwind) for component workflows.
- Check support at caniemail.com before using any CSS feature.

## 3. Content rules
- Real text, not images of text; meaningful `alt` on every image (images off by default in many clients); set image `width`/`height` attributes.
- Bulletproof buttons: padded `<a>` inside a table cell (VML for rounded buttons in Outlook if needed).
- Gmail clips messages over ~102 KB: keep HTML lean (gated: unconfirmed, Google does not publish this limit; vendor help pages such as Mailchimp state about 102 KB of HTML).
- Dark mode: some clients invert colours automatically; provide `prefers-color-scheme` styles for Apple Mail/Outlook.com, avoid transparent PNG logos with dark text, test inverted results.
- Accessibility: `lang`, logical reading order, headings in text, 14px+ text, sufficient contrast.

## 4. Test
Litmus or Email on Acid previews across clients, plus real sends to Gmail (web, iOS, Android), Apple Mail, Outlook (Windows classic and new), Outlook.com. Run a spam check and confirm plain-text alternative.

## Verify
- [ ] Renders correctly in classic Outlook for Windows and Gmail mobile; readable with images off; under 102 KB.

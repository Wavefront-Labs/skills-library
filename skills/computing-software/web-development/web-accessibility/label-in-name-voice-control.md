---
id: computing-software.web-development.web-accessibility.label-in-name-voice-control
name: label-in-name-voice-control
category: computing-software
field: web-development
product: web-accessibility
tags: [input-modalities, pointer-accessibility, label-in-name, wcag-2-5-3, voice-control, accessible-name, aria-label-mismatch, dragon-voice-control]
level: practitioner
status: verified
description: "Meeting WCAG 2.5.3 Label in Name: accessible names that contain the visible label text (ideally first) so voice control commands like 'click Search' work."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html
  - https://support.apple.com/guide/mac-help/use-voice-control-commands-mh40719/mac
  - https://www.w3.org/TR/accname-1.2/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Label in name (voice control)

**Goal:** speech-input users can activate controls by saying the text they see.

## 1. The rule (2.5.3, A)
For controls with visible text labels, the **accessible name contains the visible text**. Best practice (WCAG note): the name **starts with** the visible text, matching word order. Text used symbolically (a bold "B" icon) is not a visible label for this criterion.

## 2. Common failures
```html
<!-- visible "Search", name "Find products" - saying "click Search" fails -->
<button aria-label="Find products">Search</button>
<!-- visible "Read more", name "Article: Winter tyres" -->
<a href="/a" aria-label="Article: Winter tyres">Read more</a>
<!-- visible label "Email", aria-label overrides it -->
<label for="e">Email</label><input id="e" aria-label="Your email address">
```

## 3. Fixes
- Remove the `aria-label`; let the visible text be the name.
- Extend rather than replace: `aria-label="Search products"` for visible "Search", or append hidden text: `Read more<span class="visually-hidden"> about winter tyres</span>`.
- Use `aria-describedby` for extra info instead of changing the name.
- Punctuation/case differences and symbols are generally fine to ignore ("Next >" vs name "Next"); WCAG treats purely symbolic characters as not being text labels.

## 4. Icon-only controls
No visible text label, so 2.5.3 doesn't strictly apply - but use the name people would guess from the icon/tooltip ("Search", "Close", "Menu"), and match the `title`/tooltip text.

## 5. Test
- Chrome DevTools Accessibility pane / Firefox Accessibility Inspector: compare "Name" with visible text.
- macOS/iOS Voice Control ("Show names"), Windows Voice Access, Dragon: say "click <visible text>".
- axe rule `label-content-name-mismatch`: tagged `experimental` and off by default in axe-core 4.13 (enable with `withRules`), on by default in 4.14. It only checks controls named from content (it flagged `<button aria-label="Find products">Search</button>` but not the `<input aria-label>` plus `<label>` example above), so check inputs by hand.

## Verify
- [ ] Every control's computed name starts with its visible label.
- [ ] Voice Control "click <visible label>" activates each primary control.
- [ ] No `aria-label` on elements whose visible text is already a good name.

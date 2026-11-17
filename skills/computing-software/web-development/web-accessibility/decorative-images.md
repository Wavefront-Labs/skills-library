---
id: computing-software.web-development.web-accessibility.decorative-images
name: decorative-images
category: computing-software
field: web-development
product: web-accessibility
tags: [text-alternatives, decorative-images, alt-empty, aria-hidden, wcag-1-1-1]
level: practitioner
status: verified
description: "Hiding decorative images from assistive technology correctly: alt='' vs missing alt, CSS backgrounds, decorative SVG and icons, and deciding when an image is truly decorative."
sources:
  - https://www.w3.org/WAI/tutorials/images/decorative/
  - https://www.w3.org/WAI/WCAG22/Techniques/html/H67
  - https://www.w3.org/WAI/WCAG22/Techniques/css/C9
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decorative images

## 1. What counts as decorative
- Purely visual flourishes, dividers, background textures.
- Images whose information is already in adjacent text (icon next to the word "Download", a portrait beside the person's name).
- Stock photos that add ambience but no information.
Test: if removing the image loses no information or function, it's decorative.

## 2. Markup
| Type | Hide with |
|---|---|
| `<img>` | `alt=""` (empty, no space). **Never omit alt** - some screen readers then announce the file name (W3C images tutorial). |
| Inline SVG | `aria-hidden="true"` (plus `focusable="false"` for legacy IE/Edge) |
| Icon font / `<i>` icons | `aria-hidden="true"` on the element |
| CSS `background-image`, `::before` content | already ignored... except generated `content` text is read - use `content: "★" / ""` (alt text syntax) to silence it |
| `<figure>` decorative | just the img with `alt=""`; drop figcaption |
Don't add `role="presentation"` to an `<img>` that has empty alt - redundant; and never put `alt=""` on an image that is the only content of a link or button (the control loses its name).

## 3. Common mistakes
- `alt=" "` (space) - Chromium exposes it as a named image (name is one space) instead of ignoring it (run); use truly empty.
- `alt="decorative"`, `alt="spacer"`, `alt="image"` - noise.
- Hiding images that carry the only label of a control.
- `aria-hidden="true"` on a focusable element (it stays in tab order but becomes silent).
- Marking meaningful charts as decorative to pass automated checks.

## 4. CMS
Provide an explicit "This image is decorative" checkbox that outputs `alt=""`, so editors make a decision instead of skipping the field.

## Verify
axe `image-alt`, `role-img-alt`, `svg-img-alt`; screen reader image navigation (NVDA `G`) skips decorative images and announces meaningful ones.

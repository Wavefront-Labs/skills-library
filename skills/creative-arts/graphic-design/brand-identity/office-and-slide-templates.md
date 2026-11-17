---
id: creative-arts.graphic-design.brand-identity.office-and-slide-templates
name: office-and-slide-templates
category: creative-arts
field: graphic-design
product: brand-identity
tags: [graphic-design, brand-identity, brand-assets, slide-template, powerpoint-template, potx, dotx, google-slides-template, slide-master, theme-colours, theme-fonts, word-template]
level: practitioner
status: draft
description: "Build brand PowerPoint, Word and Google Slides templates: slide masters and layouts, theme colours and fonts, placeholders, locked logos, and testing them with real staff content."
sources:
  - https://support.microsoft.com/en-us/office/create-and-save-a-powerpoint-template-ee4429ad-2a74-4100-82f7-50f8169c8aca
  - https://support.google.com/docs/answer/1705254
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Office and slide templates

**Goal:** templates that staff use to make on-brand decks and documents without breaking them, with the
brand built into the theme rather than pasted on slides.

## PowerPoint (.potx)
1. View > **Slide Master**. Set slide size (16:9, 13.33 x 7.5 in).
2. **Theme Colors** (Design > Variants > Colors > Customize): Text/Background Dark 1, Light 1, Dark 2, Light 2,
   **Accent 1-6** (chart colours use these in order), Hyperlink, Followed Hyperlink. Use brand colours with
   good contrast; charts will pick them automatically.
3. **Theme Fonts:** heading and body. If brand fonts are not on staff machines, use a system font fallback
   or embed fonts (File > Options > Save > Embed fonts; TrueType only, licence must allow).
4. **Layouts:** title, section divider, title + content, two content, image + text, quote, chart, closing.
   Use placeholders (text, picture, chart, table) so content stays on grid; name layouts clearly.
5. Logo and fixed elements on the master or layouts, not on slides (cannot be moved by accident).
6. Save as **PowerPoint Template (.potx)**; distribute via SharePoint organisation assets so it appears in
   File > New.

## Word (.dotx)
- Styles (Normal, Heading 1-3, Title, Caption, List Bullet) mapped to brand type; theme colours and fonts;
  headers and footers with logo; content controls for fill-in fields. Save as .dotx.

## Google Slides
- Slide > Edit theme: master, layouts, theme colours. Google Fonts or Google-available fonts only; share as
  a template in the organisation's template gallery.

## Testing
- Give the template to two staff members with a real deck to build. Fix what breaks (text overflowing
  placeholders, image cropping, chart colours).

## Gotchas
- Text boxes added manually instead of placeholders ignore the theme; teach "Reset" (Home > Reset).
- Brand fonts substituted on other machines reflow everything; choose fallbacks on purpose.
- Too many layouts confuse users; 10-15 is plenty.

## Verify
- [ ] New deck from the template: every layout uses theme fonts, colours and placeholders.
- [ ] Charts default to brand accent colours in the right order.

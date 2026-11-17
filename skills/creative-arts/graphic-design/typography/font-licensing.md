---
id: creative-arts.graphic-design.typography.font-licensing
name: font-licensing
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, opentype, font-management, font-licensing, eula, desktop-licence, webfont-licence, app-embedding, ebook-licence, sil-ofl, adobe-fonts-licence, logo-use]
level: practitioner
status: draft
description: "Read and apply font licences: desktop, web, app, ebook and broadcast use, logo and trademark use, client handoff and printers, Adobe Fonts and Google Fonts (OFL) terms."
sources:
  - https://openfontlicense.org/
  - https://helpx.adobe.com/fonts/using/font-licensing.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Font licensing

**Goal:** every font in a project is licensed for every way the project uses it - before the client launches.

## Licence types (names vary by foundry; read the EULA)
| Use | Licence usually needed | Typical metric |
|---|---|---|
| Installing to design print/static images (incl. logos as outlines) | **Desktop** | number of users/computers |
| Websites via @font-face | **Web** | pageviews/month or domains |
| Embedding in iOS/Android/desktop apps | **App** | number of apps/titles |
| EPUB/ebooks with embedded fonts | **ePub/Digital publication** | titles |
| TV, film, streaming titles | **Broadcast** | productions/audience |
| Embedding in editable PDFs, server-side generation, games, products for sale (templates, merch with type as main feature) | specific or extended licences | varies |

## Common questions
- **Logos:** most desktop EULAs allow using the font to create a logo (outlined artwork). Some require an extended
  licence for trademark registration or prohibit modification - check. Custom-lettered logos avoid the issue.
- **Client handoff:** the client must buy their own licence to edit files or produce new materials; you cannot
  pass your licensed font files to them. Clarify in the proposal who buys fonts.
- **Printers/service bureaus:** many EULAs allow sending fonts to a printer for output of your job only.
- **PDF embedding:** usually allowed for print and view-only (subset); editable/form-field embedding may not be.

## Free and subscription fonts
- **SIL Open Font License (OFL)** (most Google Fonts): free for any use including commercial, web, apps, logos;
  you may not sell the fonts alone; modified versions must not use reserved font names.
- **Adobe Fonts:** included with Creative Cloud for personal and commercial projects, desktop and web
  (via Adobe's web projects); fonts cannot be sent to clients/printers as files, and app embedding or broadcast may
  need separate licences for some foundries. Check the font page's licensing notes.
- "Free for personal use" fonts from download sites are not licensed for client work.

## Practice
- Keep a **font register** per project: font, foundry, licence type, quantity, who holds it, proof of purchase.
- Audit before launch: list fonts in use (Find Font, CSS) and match against licences.

## Verify
- [ ] Every font's licence covers every use (print, web, app, video) in the project.
- [ ] Client knows which licences they must hold; register stored with the project.

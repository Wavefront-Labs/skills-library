---
id: creative-arts.graphic-design.adobe-indesign.snippets-and-library-assets
name: snippets-and-library-assets
category: creative-arts
field: graphic-design
product: adobe-indesign
tags: [graphic-design, adobe-indesign, indesign, indesign-snippets, idms, object-library, indl, cc-libraries, reusable-layout-items, indesign-automation]
level: practitioner
status: draft
description: "Reuse layout pieces in InDesign as snippets (IDMS), object libraries (INDL) and CC Library text and graphics, with original position and styles preserved."
sources:
  - https://helpx.adobe.com/indesign/using/snippets.html
  - https://helpx.adobe.com/indesign/using/object-libraries.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Snippets and library assets

**Goal:** frequently reused page items (ad boxes, sidebars, product modules, legal blocks) kept in one
place and dropped into any document with their styles intact.

## Snippets (.idms)
- Select page items, File > Export > **InDesign Snippet**, or drag items from the page to the desktop or a
  folder. The IDMS file carries the items, their styles, swatches and links (as references).
- Place with File > Place or drag in. Alt/Option-drag (or Preferences > File Handling > Snippet Import:
  **Original Location**) puts items at their original coordinates instead of the cursor.
- Snippets are XML; scripts and automated publishing systems generate them.

## Object libraries (.indl)
- File > New > **Library**. Drag items into the panel; Item Information stores name, type, description
  for search. Library > **Show Subset** filters by name or keywords.
- Placing from a library keeps the original position option (Place Item(s)).
- Libraries are local files; share via a server folder (one user editing at a time).

## CC Libraries
- Drag text frames and groups into the CC Libraries panel: they are stored as snippets in the cloud and
  available to the team. Text assets placed this way keep styles.
- Better for distributed teams than INDL; see the cc-libraries-for-brand-assets skill.

## Style conflicts
- When a snippet's style names match the target document's, the **target** definition wins by default and
  the item restyles; mismatched names import extra styles. Keep a shared style naming standard.

## Gotchas
- Snippets do not embed images; links can go missing on another machine. Package images with the snippet or
  embed small graphics.
- Fonts are not included; the receiving designer needs them.
- Old INDL libraries can become corrupt if opened by several people; keep a backup.

## Verify
- [ ] Placing the snippet in a fresh document reproduces it with correct styles and links.
- [ ] Original-location placement lands on the expected coordinates.

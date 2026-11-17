---
id: creative-arts.graphic-design.typography.widows-orphans-and-runts
name: widows-orphans-and-runts
category: creative-arts
field: graphic-design
product: typography
tags: [graphic-design, typography, justification, text-alignment, widows-and-orphans, runts, keep-options, keep-lines-together, keep-with-next, pagination, copyfitting]
level: practitioner
status: draft
description: "Prevent widows, orphans and runts in typeset text: definitions, InDesign Keep Options, no-break rules for last lines, and the order of fixes when pages will not cooperate."
sources:
  - https://helpx.adobe.com/indesign/using/text-composition.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Widows, orphans and runts

**Goal:** no stray single lines at the tops and bottoms of columns, and no single short words alone on a paragraph's last line.

## Definitions (terms vary; agree them with your editor)
- **Widow:** the last line of a paragraph stranded at the top of the next column or page (Bringhurst, Lupton).
- **Orphan:** the first line of a paragraph left alone at the bottom of a column or page.
- **Runt** (some call it a widow too): a very short last line - often one word or part of a hyphenated word - at
  the end of a paragraph.
Mnemonic: "an orphan is left behind, a widow goes on alone".

## Automatic prevention (InDesign Paragraph Style > Keep Options)
- **Keep Lines Together:** At Start/End of Paragraph: Start **2** lines, End **2** lines - prevents orphans and widows.
- **Keep with Next:** headings 2-3 lines, so a heading never sits at the foot of a column.
- **Start Paragraph:** Anywhere / In Next Column / On Next Page / On Next Odd Page (chapter openers).
- Preferences > Composition > **Highlight Keep Violations** shows where the rules were broken because they could not be met.
- **Runts:** a GREP style `\S+\s\S+$` (or a No Break on the last two words) keeps at least two words on the last
  line (see GREP styles skill). In CSS, `text-wrap: pretty` reduces runts.

## Fixing remaining problems (in order of preference)
1. **Edit copy** (cut or add a few words) - common in magazines; ask the editor.
2. **Tracking** the paragraph -5 to +5 to gain or lose a line (never visible amounts; same value for a whole paragraph).
3. **Discretionary hyphens or No Break** on word pairs.
4. Adjust image size or spacing above headings slightly (keeping the baseline grid).
5. Allow facing columns or pages to run one line long or short **in pairs** (spreads must balance) - a
  book-typesetting convention (Bringhurst).

## Gotchas
- Keep options can create gaps at the bottom of columns; in justified vertical layouts this looks worse than the widow.
- Fixes must be done last, after copy is final - any edit reflows.

## Verify
- [ ] Keep violations highlighting shows none (or accepted ones).
- [ ] No single-word last lines in body text; headings never at column bottoms.

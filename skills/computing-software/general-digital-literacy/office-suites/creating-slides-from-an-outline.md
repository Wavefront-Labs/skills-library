---
id: computing-software.general-digital-literacy.office-suites.creating-slides-from-an-outline
name: creating-slides-from-an-outline
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, pres-building, outline-to-slides, outline-view, powerpoint]
level: intro
status: docs-checked
description: "Turn a Word outline or bullet list into PowerPoint slides with Outline view, Slides from Outline, Word's Export to PowerPoint, or Copilot, keeping headings as slide titles."
sources:
  - https://support.microsoft.com/en-us/powerpoint/create-and-print-a-presentation-in-outline-view
  - https://support.microsoft.com/en-us/office/create-a-powerpoint-presentation-from-an-outline-f6294909-04e9-4020-b9a8-4587b112692c
  - https://support.microsoft.com/en-us/office/export-word-documents-to-powerpoint-presentations-51c3d683-0fc9-471e-9d36-0bbba6dca2dd
  - https://support.microsoft.com/en-us/office/prepare-your-presentation-with-microsoft-365-copilot-7f06429e-c0c2-4819-8119-b519ad599796
  - https://support.microsoft.com/en-us/accessibility/powerpoint/make-your-powerpoint-presentations-accessible-to-people-with-disabilities
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Create slides from an outline

## Type the outline in PowerPoint
- **View > Outline** (Presentation Views group). The first text you type is a slide title. **Enter** starts a new line at the same level, **Tab** demotes it one level (a bullet), **Shift+Tab** promotes it (back to a new slide title).
- Fast way to draft a whole talk before designing anything.

## Import from Word (desktop PowerPoint only)
1. In Word, use **Heading 1** for each slide title and **Heading 2** for its bullets. Text in the Normal style is not sent to PowerPoint.
2. Save and close the Word file (it must be closed to import).
3. PowerPoint: **Home > New Slide > Slides from Outline** and pick the file. Windows accepts .docx, .rtf and .txt (indented lines; unindented lines become slide titles). PowerPoint for Mac imports only Rich Text Format (.rtf).
4. Select the new slides, **Home > Reset** so the placeholders take the theme's fonts and formatting.
- Not available in PowerPoint for the web.

## Word for the web: Export to PowerPoint
- **File > Export > Export to PowerPoint presentation**, choose a design theme, **Export**. Headings become slide titles; the document should contain only text.
- Microsoft says this export option is being deprecated and will be removed from Word.

## Copilot
- Copilot in PowerPoint: type *Create presentation from file* and pick the Word document; it drafts slides with images and speaker notes. Review every slide; AI summaries drop and invent points.

## Gotchas
- If you get one slide per paragraph, the Word file has no Heading 1 or Heading 2 styles.
- Imported slides keep Word formatting until you reset them.
- An outline with eight bullets per slide is still a bad slide: split or cut.

## Verify
- [ ] Slide count equals the number of Heading 1 lines and slides use the theme's fonts.

## Checked
2026-10-27, against Microsoft Support pages for PowerPoint for Microsoft 365 and PowerPoint 2016-2024 (Outline view; Create a presentation from an outline; Export Word documents to PowerPoint; Prepare your presentation with Copilot; accessibility guide for the Home > Reset command). Confirmed: Outline view Enter/Tab/Shift+Tab behaviour, Slides from Outline path and file types (.docx/.rtf/.txt, Mac RTF only, not on the web), the Word-must-be-closed rule, the Export to PowerPoint path and its deprecation notice, and the Copilot "Create presentation from file" prompt.
Method: documentation only; no commands were run.

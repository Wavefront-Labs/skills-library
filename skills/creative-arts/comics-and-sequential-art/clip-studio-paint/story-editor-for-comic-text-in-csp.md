---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.story-editor-for-comic-text-in-csp
name: story-editor-for-comic-text-in-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-comic-project, csp-page-management, csp-story-editor, story-file, text-management, clip-studio-paint-ex]
level: practitioner
status: draft
description: "Use Clip Studio Paint EX's Story Editor to enter, review and edit all dialogue across a multi-page story: opening it, pasting a script, insert modes and syncing with pages."
sources:
  - https://tips.clip-studio.com/en-us/articles/849
  - https://tips.clip-studio.com/en-us/articles/2875
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Story editor for text (CSP EX)

The **Story Editor** (EX only) shows every text layer in a multi-page story file in one scrollable
document, page by page, so you can letter and proof dialogue without opening each page.

## Open it
- Open the story's `.cmc` file (page manager), then **Story > Text Management > Open Story Editor**.
- The left column lists pages; each text block maps to a text layer on that page.

## Entering a script
1. Write the script in a text editor; keep one balloon per paragraph and a blank line between them.
2. In the Story Editor, put the cursor on the target page and paste (Edit > Paste).
3. Set **How to insert new text**: the default adds lines into a single text layer per page; choose
   **Always create new layer** so each paragraph becomes its own text layer (one per balloon).
4. Open each page and drag the text layers onto their balloons, or create balloons from text.

## Editing
- Edits in the Story Editor update the text layers on pages, and vice versa, once saved.
- Use it as a proofreading view: typos, consistent character names, punctuation.
- Font and size changes can be applied in bulk to selected text blocks.

## Gotchas
- PRO has no Story Editor; text must be edited per page.
- Pages must be part of the story file (not separate .clip files opened alone).
- Pasting rich text from a word processor brings smart quotes and special dashes; check the font has them.

## Verify
- [ ] Every page shows the expected text blocks; no orphan text left in the default single layer.
- [ ] After saving, open a page and confirm layers updated.

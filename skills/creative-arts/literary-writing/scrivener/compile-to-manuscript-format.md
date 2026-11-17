---
id: creative-arts.literary-writing.scrivener.compile-to-manuscript-format
name: compile-to-manuscript-format
category: creative-arts
field: literary-writing
product: scrivener
tags: [literary-writing, scrivener, scrivener-3, compile, compile-format, section-types, section-layouts, binder, corkboard, outliner, snapshots, standard-manuscript-format, shunn, manuscript-submission, docx, epub, pdf, word-count-targets, front-matter, novel-writing, backup, writing-software]
level: practitioner
status: draft
description: "Organise a book in Scrivener 3's binder and compile it to standard manuscript format DOCX/PDF: section types, layouts, front matter, placeholders, snapshots and backups."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compile to manuscript format — Scrivener from binder to submission file

**Goal:** write in small binder documents (scenes), then produce a correctly
formatted manuscript (e.g. standard manuscript format for agents or magazines) or an
ebook with one Compile, without hand-formatting. Based on Scrivener 3 (macOS/Windows);
menu names may differ slightly between platforms and versions.

## 1. Structure the binder for compile
- One **text document per scene**, grouped in **folders per chapter** (or a single
  document per chapter if you prefer). Folders can hold text too, but keep it simple.
- **Don't type chapter titles** into the text — let Compile generate them ("Chapter
  One") from the folder structure, so reordering renumbers automatically.
- Put notes, research and cut scenes outside the **Draft/Manuscript** folder (in
  Research or a "Cut" folder); only the Draft folder compiles by default. Untick
  "Include in Compile" in the Inspector for drafts you want to keep inside.
- Use the **corkboard** (synopsis cards) and **outliner** to plan and reorder; set
  **targets** (Project › Project Targets) for manuscript and session word counts.

## 2. Section types (Scrivener 3)
Project › Project Settings › Section Types: create types such as *Chapter*, *Scene*,
*Front Matter*. Then set **default types by structure** (e.g. folders at level 1 =
Chapter, documents at level 2 = Scene). Section types say *what* a document is; compile
formats decide *how* each type looks.

## 3. Compile
File › Compile (Cmd/Ctrl+Opt/Shift+E — check your shortcut):
1. **Compile for:** choose output — Word (.docx), PDF, ePub 3, Kindle, etc.
2. **Format:** pick a built-in format; *Manuscript (Times)* / *Manuscript (Courier)*
   approximate standard manuscript format; *Shunn Modern/Classic* manuscript formats are
   included in recent versions (based on William Shunn's widely used guide).
3. **Assign Section Layouts:** button at the top of the middle panel — map each section
   type to a layout (Chapter → "Chapter Heading", Scene → "Section Text").
4. **Contents (right panel):** confirm which documents compile; add front matter
   (title page) from the format's front-matter options or your own Front Matter folder.
5. **Placeholders/metadata:** set title, author and contact details in Project ›
   Project Properties / Metadata; formats insert them via placeholders like `<$projecttitle>`,
   `<$wc100>` (word count rounded to nearest 100 — check exact tags in the manual).
6. Compile; open the result in Word/a PDF reader and check.

## 4. Typical standard manuscript format (verify per market)
12 pt Times New Roman or Courier, double-spaced, 1-inch margins, first-line indent
0.5 in (no extra space between paragraphs), header with surname / short title / page
number, contact info and word count on page one, chapters starting on a new page about a
third of the way down, scene breaks marked with a centred `#`. **Each agent/magazine's
guidelines override this.**

## 5. Customising a format
Duplicate a built-in format (right-click › Duplicate & Edit) rather than editing it
directly. In the format editor: Section Layouts (title prefix, numbering like
"Chapter <$t>" for spelled-out numbers), Separators (scene break as `#`), Page Settings
(headers/footers), and Text Replacements if needed.

## 6. Safety: snapshots and backups
- **Snapshots** (Documents › Snapshots › Take Snapshot, or Cmd/Ctrl+5): save a version of
  a document before heavy revision; compare later.
- **Automatic backups:** File/Preferences › Backup — back up on close, keep several,
  zipped, to a folder on a different drive or cloud location.
- If syncing via Dropbox etc., close Scrivener on one device before opening on another —
  projects are folder bundles and simultaneous edits can corrupt them.

## Gotchas
- **Manual formatting in the editor** (fonts, sizes) can leak into output; formats
  normally override, but check "Override text and notes formatting" in the format.
- **Chapter titles typed in text** duplicate the generated titles.
- **Missing scene separators** happen when sections aren't assigned layouts.
- Shortcuts, menu names and placeholder tags are written from memory of Scrivener 3
  and not re-verified in the current build — confirm against the built-in manual (Help).

## Verify
- [ ] Draft folder contains only content to compile; chapters as folders, scenes as documents.
- [ ] Section types assigned by structure; every type mapped to a layout.
- [ ] Compiled DOCX/PDF matches the target market's formatting guidelines.
- [ ] Title page shows correct title, author, contact and word count.
- [ ] Automatic backups go to a second location; snapshot taken before big revisions.

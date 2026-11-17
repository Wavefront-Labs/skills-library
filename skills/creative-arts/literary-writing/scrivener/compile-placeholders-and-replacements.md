---
id: creative-arts.literary-writing.scrivener.compile-placeholders-and-replacements
name: compile-placeholders-and-replacements
category: creative-arts
field: literary-writing
product: scrivener
tags: [literary-writing, scrivener, scrivener-3, compile, scrivener-compile, compile-placeholders, compile-replacements, placeholder-tags, auto-numbering, word-count-placeholder, project-properties, search-and-replace]
level: practitioner
status: draft
description: "Use Scrivener compile placeholders (chapter numbers, title, author, rounded word count) and compile-time replacements to generate front matter and fix text automatically in output."
sources: ["https://www.literatureandlatte.com/learn-and-support/user-guides"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Placeholders and replacements

**Goal:** let Compile write the things that change — chapter numbers, word counts,
author details — and transform text in the output without touching your drafts.
Scrivener 3. The authoritative list of placeholder tags is in the user manual
(and **Help > Placeholder Tags List** on some versions); verify exact tags there.

## Placeholders (examples to confirm in your version's list)
| Tag (typical) | Inserts |
|---|---|
| `<$n>` | Auto-incrementing number (e.g., chapter numbers) |
| `<$w>` / `<$W>` | Number as a word ("one" / "ONE") |
| `<$r>` / `<$R>` | Roman numerals |
| `<$t>` / `<$title>` | Document title |
| `<$projecttitle>` | Project title (from Project Properties) |
| `<$fullname>`, `<$surname>` | Author name fields |
| `<$wc100>` | Draft word count rounded to nearest 100 (for manuscript front pages) |
| `<$date>` | Compile date |

Where they go:
- **Section layout titles/prefixes**: "Chapter `<$w>`" builds "Chapter One" — so
  reordering chapters renumbers automatically.
- **Front matter documents** (title page): name, contact, `<$wc100>` words.
- **Header/footer** settings in PDF/print formats: `<$surname> / <$abbr_projecttitle> / <$p>`
  style headers (check tag names in the list).

Fill author name, title, abbreviated title etc. in **Project > Project Settings >
Project Properties** so placeholders resolve.

## Replacements (compile-time find and replace)
In the compile format (format editor) or the compile overview, the **Replacements**
pane lets you specify text to replace in the output only:
- Replace `--` with an em dash; strip editorial markers like `TK` or `[[ ]]` notes.
- Swap a code name for a final character name at compile ("Character A" -> "Anna").
- Options for case sensitivity and whole words.
Your binder text stays unchanged.

## Gotchas
- Typing chapter numbers by hand in titles — then renumbering breaks. Use placeholders.
- Placeholders inside text that should print literally (rare) — check output.
- Replacements that catch unintended matches; enable whole-word matching and test.

## Verify
- [ ] Chapter headings use number placeholders.
- [ ] Title page pulls name and rounded word count from placeholders.
- [ ] Replacements tested on a compiled sample; no unintended changes.

---
id: computing-software.general-digital-literacy.office-suites.word-count-and-readability-statistics
name: word-count-and-readability-statistics
category: computing-software
field: general-digital-literacy
product: office-suites
tags: [office-suites, word-processing, word-count, readability-statistics, flesch-kincaid, character-count, proofing]
level: intro
status: docs-checked
description: "Check word and character counts for a whole document or a selection in Word and Google Docs, and read Flesch readability scores in Word."
sources:
  - https://support.microsoft.com/en-us/office/show-word-count-3c9e6a11-a04d-43b4-977c-563a0e0d5da3
  - https://support.microsoft.com/en-us/office/get-your-document-s-readability-and-level-statistics-85b4969e-e80a-4777-8dd3-f7fc3c8b3fd2
  - https://support.google.com/docs/answer/39003
  - https://support.google.com/docs/answer/179738
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Word count and readability statistics

**Goal:** prove a piece is within a limit and judge whether it is easy enough to read.

## Word
- The **status bar** shows the word count; select text to see the count for the selection alongside the whole document. Click the count to open the Word Count box with pages, characters, paragraphs and lines (described for Word for Mac). In Word for the web, **Review > Word Count** toggles the live count.
- Readability: **Home > Editor > Document stats** (Microsoft 365), or **File > Options > Proofing**, tick **Show readability statistics** then run Spelling & Grammar. Flesch Reading Ease is on a 100-point scale where higher is easier, with 60 to 70 the target for most files; Flesch-Kincaid Grade Level of 8.0 means an eighth grader can understand it, and the recommended score is about 7.0 to 8.0.

## Google Docs
- **Tools > Word count** (Ctrl+Shift+C on Windows, Command+Shift+C on Mac); tick **Display word count while typing** for a live box at bottom left. Select text to count a portion.
- Unless you select a section, the count excludes headers, footers and footnotes.
- Docs has no readability score in this help page; paste the text into Word if you need one (avoid pasting confidential text into web tools).

## Gotchas
- Tools disagree: hyphenated words, URLs and numbers are counted differently. If a portal enforces a limit, check in the portal's own box and leave a margin.
- Character limits on web forms usually count spaces and line breaks.
- Readability formulas only measure sentence and word length; short sentences with jargon still read badly.

## Verify
- [ ] Count matches the rule (check what the limit includes).
- [ ] Reading Ease suits the audience.

## Checked

2026-10-27. Microsoft Support 'Show word count' and readability statistics pages, Google Docs 'Count the words in a document' and keyboard shortcuts page (read 2026-10-27). Confirmed status bar and selection counts, Document stats path, 60-70 and 7.0-8.0 targets, Google Tools > Word count, live counter, exclusions, Ctrl+Shift+C. Removed: Word Ctrl+Shift+G, the 'Include textboxes, footnotes and endnotes' option, the claim that Docs counts footnotes separately (it excludes them), and the LibreOffice section (not checked).

Method: documentation only; no commands were run.

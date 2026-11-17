---
id: computing-software.software-engineering.javascript.js-grapheme-segmenter
name: js-grapheme-segmenter
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, intl-segmenter, js-strings]
level: advanced
status: docs-checked
description: "Use Intl.Segmenter for locale-sensitive word, sentence and grapheme segmentation instead of split(\" \")."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text segmentation with Intl.Segmenter

- `Intl.Segmenter` does locale-sensitive text segmentation, giving meaningful items (graphemes, words or sentences) from a string.
- `new Intl.Segmenter("ja-JP", { granularity: "word" })` then `.segment(str)` returns an iterable `Segments` object; `Array.from(segments)` gives entries like `{ segment, index, input, isWordLike }`.
- `str.split(" ")` fails for languages that do not separate words with spaces (Japanese, Chinese, Thai, Lao, Khmer, Myanmar), so pass the right locale.
- `resolvedOptions()` shows the locale and granularity actually used; `Intl.Segmenter.supportedLocalesOf()` lists supported locales without falling back to the default.
- Check browser and runtime support before relying on it (see MDN's compatibility table).

Self-check: segmenting `"Que ma joie demeure"` with `"fr"` and `granularity: "word"` yields `"Que"` then `" "` first (MDN example).

## Checked

Date: 2026-11-03. Confirmed on MDN Global_Objects/Intl/Segmenter: purpose, word granularity example, Segments and entry fields, the split(" ") warning, resolvedOptions, supportedLocalesOf, French example. Removed as not stated there: the `"grapheme"` option string and emoji/ZWJ counting claims, the character counter and truncation recipes, surrogate-pair advice for slice, and the emoji length figures.

Method: documentation only; no commands were run.

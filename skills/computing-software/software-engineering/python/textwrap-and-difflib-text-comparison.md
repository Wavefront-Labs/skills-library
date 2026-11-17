---
id: computing-software.software-engineering.python.textwrap-and-difflib-text-comparison
name: textwrap-and-difflib-text-comparison
category: computing-software
field: software-engineering
product: python
tags: [python, py-text-processing, textwrap-difflib, textwrap, difflib, unified-diff, sequencematcher, get-close-matches, dedent]
level: practitioner
status: docs-checked
description: "Wrap, indent and dedent text with textwrap and compare texts with difflib: unified diffs, SequenceMatcher ratios, fuzzy matching and test failure diffs."
sources: ["https://docs.python.org/3/library/textwrap.html", "https://docs.python.org/3/library/difflib.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# textwrap and difflib

## textwrap
```python
import textwrap
textwrap.dedent("""\
    SELECT *
      FROM t
""")                                            # strips common leading whitespace (multi-line literals in indented code)
textwrap.fill(long_text, width=72)               # one wrapped paragraph string
textwrap.wrap(long_text, width=72, break_long_words=False)   # list of lines
textwrap.shorten("Hello   wide world", width=14, placeholder="...")  # 'Hello wide...'
textwrap.indent("a\nb", "> ")                    # quote-style prefix; skips blank lines by default
```

## difflib
```python
import difflib
a, b = old.splitlines(keepends=True), new.splitlines(keepends=True)
print("".join(difflib.unified_diff(a, b, fromfile="old.txt", tofile="new.txt", n=3)))
difflib.ndiff(a, b)                              # shows intraline hints with ? lines
difflib.HtmlDiff().make_file(a, b)               # side-by-side HTML report

sm = difflib.SequenceMatcher(None, "kitten", "sitting")
sm.ratio()                                       # 0.615..., 2*matches/total
sm.get_opcodes()                                 # [('replace',0,1,0,1), ...] edit script
difflib.get_close_matches("pyhton", ["python", "pylint"], n=1, cutoff=0.6)   # did-you-mean suggestions
```

## Gotchas
- `SequenceMatcher` finds the longest contiguous matching blocks, not minimal edit distance; ratios are not Levenshtein. Its worst case is quadratic time; by default (`autojunk=True`) popular items are treated as junk when the second sequence has 200 or more items, so pass `autojunk=False` if you need exact results there.
- `splitlines(keepends=True)` avoids spurious "No newline" differences; otherwise `unified_diff(..., lineterm="")`.
- `dedent` ignores lines that are whitespace only; tabs and spaces are not treated as equal, so mixed indentation will not dedent consistently.
- `wrap` replaces each whitespace character with a space when `replace_whitespace` is true (default); `drop_whitespace` (default true) drops whitespace at line starts and ends.
- `shorten` collapses whitespace first, and `drop_whitespace` and `replace_whitespace` have no effect on it.

## Verify
- [ ] Apply the unified diff with `patch` (or compare `a`/`b` roundtrip) to confirm a faithful output.
- [ ] Test `get_close_matches` threshold on typical typos and non-matches.

## Checked

- 2026-11-03: checked against the CPython docs `library/textwrap.rst` and `library/difflib.rst`: `wrap`/`fill`/`shorten`/`dedent`/`indent` behaviour and options, `unified_diff`, `HtmlDiff.make_file`, `SequenceMatcher` longest-contiguous-match approach, `autojunk` and the 200-item threshold, quadratic worst case, `get_close_matches` cutoff 0.6.
- Removed: wcwidth, rapidfuzz, diff-match-patch and pytest remarks.

Method: documentation only; no commands were run.

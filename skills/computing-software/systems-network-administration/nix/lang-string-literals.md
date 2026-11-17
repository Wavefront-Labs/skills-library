---
id: computing-software.systems-network-administration.nix.lang-string-literals
name: lang-string-literals
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, string-literals, indented-strings, escaping, interpolation]
level: practitioner
status: docs-checked
description: "Write Nix strings correctly: double-quoted escapes, indented strings with '' and their escapes for $ and ${, indentation stripping and bare URIs."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/language/string-literals.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Double-quoted: can span lines; `${ }` interpolates. Escape with backslash: `\"`, `\\`, `\${`; also `\n`, `\r`, `\t`. `$${` can be written literally.

Indented strings use `''`:

```
''
This is the first line.
  This is the third line.
''
```

- The minimal shared indentation is stripped (empty lines ignored when computing it).
- A newline directly after the opening `''` is ignored if the first line has no non-whitespace text.
- Prefixed tab characters are not stripped.
- Interpolation works.

Escapes in indented strings:
- `$`: `''$`
- `''`: `'''`
- newline, CR, tab: `''\n`, `''\r`, `''\t`; `''\` escapes any other character
- `${`: `''${` (for example `echo ''${PATH}` gives `echo ${PATH}`)

Gotcha: the `${` escape differs between the two string types, `"\${"` versus `''${`. Use the one matching the string type.

Indented strings suit shell scripts and config text because `''` is much rarer than `"`.

URIs per RFC 2396 appendix B can be written unquoted: `http://example.org/foo.tar.bz2` equals the quoted string.

## Checked

2026-11-04. Confirmed against the Nix manual String literals page: double-quoted escapes, `$${`, indentation stripping, the note on the first line, the tab warning, the indented-string escapes (`''$`, `'''`, `''\n`, `''\r`, `''\t`, `''${`), the differing `${` escape note, and unquoted URIs per RFC 2396 appendix B. Removed an unsourced command line.

Method: documentation only; no commands were run.

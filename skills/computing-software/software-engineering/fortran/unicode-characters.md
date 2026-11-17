---
id: computing-software.software-engineering.fortran.unicode-characters
name: unicode-characters
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, unicode-characters, fortran-strings]
level: advanced
status: draft
description: "Handle Unicode text with selected_char_kind('ISO_10646') and encoding='UTF-8' on files, knowing limits."
sources:
  - https://j3-fortran.org/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unicode and ISO_10646 characters
**Goal:** read and write wide characters.
```fortran
integer, parameter :: ucs4 = selected_char_kind('ISO_10646')
character(kind=ucs4, len=20) :: s
open (newunit=u, file='t.txt', encoding='UTF-8', status='old', action='read')
```
- Kind is -1 if unsupported; gfortran supports UCS-4 (kind 4).
- Literals: `ucs4_'text'`.
- Many programs simply treat UTF-8 as bytes in default characters; works unless you slice mid-character.
## Gotchas
- Formatted I/O of UCS-4 requires `encoding='UTF-8'` to be set at open.
- Terminals may need a UTF-8 locale for display.
## Self-check
Print the string with an accented letter and compare bytes in a hex dump.

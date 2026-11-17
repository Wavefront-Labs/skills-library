---
id: computing-software.systems-network-administration.linux.vim-motions-and-text-objects
name: vim-motions-and-text-objects
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, vim, vim-motions, text-objects, operators, vi, editing-efficiency]
level: practitioner
status: docs-checked
description: "Edit fast in vim with operator + motion/text-object grammar: word, line and paragraph motions, f/t, %, iw/aw, quote and bracket objects, counts and dot repeat."
sources:
  - https://vimhelp.org/motion.txt.html
  - https://vimhelp.org/change.txt.html
  - https://vimhelp.org/repeat.txt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vim motions and text objects

## Grammar
`[count] operator [count] motion|text-object` — operators: `d` delete, `c` change, `y` yank, `>`/`<` indent,
`gu`/`gU` case, `=` reindent, `gq` reflow. Doubling acts on the line (`dd`, `cc`, `>>`).

## Motions
| Motion | Moves |
|---|---|
| `w` `b` `e` / `W` `B` `E` | word / WORD (whitespace-delimited) |
| `0` `^` `$` | line start / first non-blank / end |
| `f,` `t,` `;` `,` | to / till a char on the line, repeat, reverse |
| `%` | matching bracket |
| `{` `}` | paragraph (blank-line separated) |
| `gg` `G` `42G` | top, bottom, line 42 |
| `*` `#` | next/previous occurrence of word under cursor |
| `H` `M` `L` | screen top/middle/bottom |
| `/pat` | search as a motion: `d/END` deletes up to END |

## Text objects (with an operator or in visual mode)
`iw`/`aw` word, `is`/`as` sentence, `ip`/`ap` paragraph, `i"`/`a"` quotes, `i(`/`a(` (`ib`), `i{`/`a{` (`iB`),
`i[`, `i<`, `it`/`at` XML/HTML tag. `i` = inside, `a` = including delimiters/whitespace.

## Sysadmin examples
```
ci"        change the quoted value: Listen "8080" → type new value
da{        delete a whole { } block in nginx config
yap        yank a paragraph (an ini section)
>ip        indent a YAML block
dt#        delete up to an inline comment
3dw / d3w  delete three words
.          repeat the last change — combine with n:  /old<Enter> cgnnew<Esc> then . . .
```

## Gotchas
- Text objects work from anywhere inside the object — no need to move to its start.
- `>` shifts by `'shiftwidth'` (default 8 columns) — for YAML set `sw=2 et` (`autocmd FileType yaml setlocal sw=2 et`).
- `gn` selects the next match of the last search and operates on it when an operator is pending, which is what makes `cgn` plus `.` work.

## Verify
- [ ] You can change a quoted value, delete a block and repeat an edit across matches without arrow keys.

## Checked

2026-10-26. Documentation checked: Vim runtime/doc help files on vim/vim master (last commit 2026-10-25, Vim 9.2 series). Confirmed: word, WORD, 0, ^, f/t/;/,, {, }, %, H/M/L, gg/G motions (motion.txt), * and # (pattern.txt), text objects iw/aw/is/as/ip/ap/i"/a"/ib/iB/i[/i</it/at (motion.txt), operators gu/gU/gq/=/>/< (change.txt), gn behaviour (visual.txt), shiftwidth default 8 (options.txt).

Method: documentation only; no commands were run.

---
id: computing-software.systems-network-administration.bash.prompt-trim-dirtrim
name: prompt-trim-dirtrim
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, prompt-trim-dirtrim, dirtrim, shell-scripting]
level: intro
status: docs-checked
description: "Shorten long working-directory paths in bash prompts using PROMPT_DIRTRIM with the w and W prompt escapes."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PROMPT_DIRTRIM
**Goal:** keep the prompt short in deep directories.
```bash
PROMPT_DIRTRIM=2          # keep the last 2 components of \w; removed ones become an ellipsis
PS1='\u@\h \w\$ '         # \w: $PWD with $HOME shown as ~
PS1='\u@\h \W\$ '         # \W: basename of $PWD
```
- If `PROMPT_DIRTRIM` is a number greater than zero it is the number of trailing directory components kept when `\w` and `\W` are expanded; the characters removed are replaced with an ellipsis.- It only changes how the prompt escapes expand, not the value of `$PWD`.
- `\w` is `$PWD` with `$HOME` abbreviated with a tilde (this form uses `PROMPT_DIRTRIM`); `\W` is the basename of `$PWD` with `$HOME` abbreviated with a tilde.
- `\$` in a prompt is `#` if the effective uid is 0, otherwise `$`.
- Set it where interactive shells read it: `~/.bashrc` is read by interactive non-login shells; a login shell reads `~/.bash_profile` (or `~/.bash_login`, `~/.profile`), which commonly sources `~/.bashrc`.

## Checked
Date: 2026-11-07
Method: Read GNU Bash manual entries for PROMPT_DIRTRIM, section 6.9 Controlling the Prompt (\w, \W, \$) and Bash Startup Files (interactive non-login and login). Trims: removed the example output `.../d/e` and the "(bash 4.0+)" version claim (neither in the manual), the claim that unset or 0 disables trimming (the manual says only "greater than zero"), and the invented "cd four levels" Verify step; "replaces the rest with `...`" became the documented "ellipsis". Searched for the relevant entries rather than reading the whole page.

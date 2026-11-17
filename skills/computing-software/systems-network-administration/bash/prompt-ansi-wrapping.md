---
id: computing-software.systems-network-administration.bash.prompt-ansi-wrapping
name: prompt-ansi-wrapping
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, prompt-ansi-wrapping, ps1-color, shell-scripting]
level: advanced
status: docs-checked
description: "Wrap non-printing ANSI colour codes in PS1 with backslash-bracket pairs so bash computes line length correctly."
sources:
  - https://www.gnu.org/software/bash/manual/bash.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Colour codes in PS1 with \[ \]
**Goal:** coloured prompts that stay aligned when the line wraps.
```bash
PS1='\[\e[1;32m\]\u@\h\[\e[0m\]:\[\e[1;34m\]\w\[\e[0m\]\$ '
# build from variables
RED='\[\e[31m\]'; RST='\[\e[0m\]'
PS1="${RED}\h${RST} \$ "
# tput version
PS1="\[$(tput setaf 2)\]\u\[$(tput sgr0)\] \$ "
```
- `\[` begins and `\]` ends a sequence of non-printing characters, which can be used to embed a terminal control sequence into the prompt. Put every colour escape between them.
- `\e` in a prompt string is an escape character; `\nnn` is the character whose ASCII code is the octal value nnn (so `\033` is escape).
- `\$` shows `#` if the effective uid is 0, otherwise `$`.
- After the prompt string is decoded it is expanded by parameter expansion, command substitution, arithmetic expansion and quote removal (subject to the `promptvars` shell option). A `$(tput ...)` inside double quotes is expanded once, when `PS1` is assigned.
- `PROMPT_COMMAND`, if set, holds a command (or each element of an array holds one) run before the primary prompt is printed.

## Checked
Date: 2026-11-07
Method: Read GNU Bash manual section 6.9 Controlling the Prompt (\e, \nnn, \[, \], \$ and the post-decode expansion paragraph), the PROMPT_COMMAND variable entry. Trims: removed the unsourced claims that missing brackets cause "history-recall overwrites", the NO_COLOR and `[[ -t 1 ]]` advice (NO_COLOR is not in the manual), the claim to use `\001`/`\002` in PROMPT_COMMAND-built strings, the claim that command substitution must not be used inside `\[ \]`, and the invented Verify step. Searched the manual for these entries rather than reading all of it.

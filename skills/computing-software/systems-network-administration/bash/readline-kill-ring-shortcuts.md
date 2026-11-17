---
id: computing-software.systems-network-administration.bash.readline-kill-ring-shortcuts
name: readline-kill-ring-shortcuts
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, readline-kill-ring-shortcuts, readline-kill-yank, shell-scripting]
level: practitioner
status: docs-checked
description: "Use bash Readline editing shortcuts: kill and yank, word and line movement, undo, history search and inputrc."
sources:
  - https://tiswww.case.edu/php/chet/readline/readline.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Readline kill ring and editing shortcuts
**Goal:** edit command lines quickly (emacs mode is the Readline default).
```
C-a / C-e         beginning / end of line       M-b / M-f   backward / forward word
C-k               kill-line (to end of line)    C-u         unix-line-discard (kill to start)
C-w               unix-word-rubout              M-d         kill-word
M-DEL             backward-kill-word            C-x Rubout  backward-kill-line
C-y / M-y         yank / yank-pop               C-_ or C-x C-u   undo
M-. or M-_        yank-last-arg                 C-r / C-s   reverse / forward history search
M-#               insert-comment                C-l         clear-screen
C-x C-r           re-read-init-file
```
- (C- = Control, M- = Meta/Alt.)
- Killing deletes text but saves it in the kill ring; consecutive kills save all the killed text together, so `C-k` twice then `C-y` yanks both. The kill ring is not line specific: text killed on an earlier line can be yanked on a later one.
- `M-y` rotates the kill ring and yanks the new top, but only right after `C-y` or `M-y`.
- Undo is incremental and remembered separately for each line; you can undo back to an empty line.
- Two `C-r` presses with no new search string reuse the last incremental search string.
- Customise in `~/.inputrc` (or the file named by `INPUTRC`; falls back to `/etc/inputrc`). `set editing-mode vi` switches to vi keys; the default is emacs.
- Self-check: type words, `C-w`, then `C-y` restores them.

## Checked
Checked 2026-11-08 against the Readline manual: Readline Killing Commands, Commands For Killing/Moving/History, Miscellaneous Commands, inputrc file and editing-mode. Removed because the cited page does not cover them: edit-line-in-$EDITOR (`C-x C-e`), `stty -ixon` for C-s, and `bind -P` / `set -o vi` (Bash-manual features).

Method: docs-only read of cited pages, 2026-11-08

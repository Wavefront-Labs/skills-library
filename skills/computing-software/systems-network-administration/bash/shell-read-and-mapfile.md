---
id: computing-software.systems-network-administration.bash.shell-read-and-mapfile
name: shell-read-and-mapfile
category: computing-software
field: systems-network-administration
product: bash
tags: [bash, sh-read-builtin, mapfile-readarray, ifs-parsing, read-delimiter]
level: practitioner
status: docs-checked
description: "Read input with read and mapfile safely: -r, IFS, delimiters, NUL-separated input and end-of-file status handling."
sources: ["https://www.gnu.org/software/bash/manual/bash.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# read and mapfile

- Always `read -r` (without it a backslash escapes the next character and is removed). The line is split into words using the characters in `IFS`, so `IFS= read -r line` keeps the line unsplit.
- Split on a delimiter: `IFS=: read -r user _ uid _ < /etc/passwd` (extra words go to the last name; the `_` discard idiom). `IFS=, read -ra fields <<< "$csv"` assigns the words to the array `fields` (`-a`); splitting is by `IFS` only, with no quote handling, so use a real parser for quoted CSV.
- `read` returns non-zero at end-of-file, so a final line without a trailing newline ends a `while read` loop even though the variable was filled; the common idiom is `while IFS= read -r l || [[ -n $l ]]; do ...`.
- NUL-separated input: `while IFS= read -r -d '' f; do ...; done < <(find . -print0)` (an empty `-d` delimiter means NUL).
- `mapfile -t lines < file` (alias `readarray`) loads lines into an array without a loop. Options: `-t` strips the trailing delimiter, `-d delim` sets the delimiter (empty means NUL), `-n count` copies at most count lines, `-s count` discards the first count lines, `-O origin` starts at an index, `-u fd` reads from a descriptor. Without `-t` the newline stays on each element. The default array is `MAPFILE`.
- Prompts and timeouts: `read -r -p "Continue? " ans` (prompt only if input is a terminal), `-t 5` timeout (status above 128 on timeout), `-s` silent (no echo on a terminal), `-n 1` returns after one character.
- Each command in a pipeline runs in its own subshell, so `read` at the end of a pipe does not set variables in your shell; feed it with redirection or process substitution instead.
- To keep a loop body from consuming the loop's input, read the loop from another descriptor (`read -u 3`, `3< file`).

## Checked
2026-11-08. Confirmed in the GNU Bash manual: read options -a -d -n -N -p -r -s -t -u, IFS splitting, exit status greater than 128 on timeout and non-zero at EOF; mapfile/readarray options and defaults; pipeline subshells. Removed: the "Bash 4+; macOS ships bash 3.2" claim and the ssh/ffmpeg `-n` advice (not in the manual); reworded the final-line item to what the manual states (EOF status).
Method: documentation only; no commands were run.

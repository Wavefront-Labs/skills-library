---
id: computing-software.systems-network-administration.syncthing.stignore-escaping-special-characters
name: stignore-escaping-special-characters
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, stignore, escape, brackets]
level: practitioner
status: docs-checked
description: "Escape brackets and braces in .stignore, including the pipe escape and #escape directive needed on Windows."
sources: ["https://docs.syncthing.net/users/ignoring.html", "https://docs.syncthing.net/users/faq.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Escaping special characters in .stignore

## The problem
Patterns are globs, so a file literally named `q[abc]x` is not matched by that text. The brackets are read as a character range and match `qax`, `qbx` and `qcx` instead.

## Unix-like systems
Escape with a backslash:

```
q\[abc\]x
\{banana\}
```

## Windows
Backslash is the path separator, so use the pipe character as the escape:

```
q|[abc|]x
|{banana|}
```
The pipe escape is available since version 2.0.0.

## One file for every OS
Put `#escape=\` at the top of the file, before any patterns. Leading comments and blank lines are fine. Then backslash is the escape character and `/` is the path separator on all systems:

```
#escape=\
/path/baz\[2\]/ex\[3\].txt
```
Each file loaded with `#include` needs its own `#escape=` line. You can pick another escape character with `#escape=X`.

## Check
Compare the pattern against the exact file name, then rescan and confirm the file is ignored or synced as intended. Remember that `//` only starts a comment at the beginning of a line.

## Checked

2026-11-09. Confirmed against the Syncthing Ignoring Files page (users/ignoring) and the FAQ usage part (users/faq-parts/usage), raw rst from syncthing/docs: the q[abc]x example and its qax/qbx/qcx matches, backslash and pipe escapes, 2.0.0 version note, #escape=X placement rule and per-#include requirement, // comment rule. Removed: nothing.

Method: documentation only; no commands were run.

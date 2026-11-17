---
id: computing-software.devops-ci-cd.earthly.earthly-earthlyignore
name: earthly-earthlyignore
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthlyignore, dockerignore, build-context, copy, filepath-match]
level: intro
status: docs-checked
description: "Exclude files from the build context sent to BuildKit with an .earthlyignore file: location, dockerignore-style syntax, Go filepath.Match terms and the remote-target limitation."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/earthlyignore.md
  - https://github.com/earthly/earthly/blob/main/docs/guides/best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# .earthlyignore

Goal: avoid sending unwanted files to the BuildKit daemon as part of the local build context.

## Rules
- The `.earthlyignore` file must sit in the same directory as the target being built.
- Syntax follows a `.dockerignore` file; matching is done with the Go `filepath.Match` function behind the scenes.
- One pattern per line; empty lines and lines starting with `#` are ignored.

## Pattern terms
```
pattern:
	{ term }
term:
	'*'         matches any sequence of non-Separator characters
	'?'         matches any single non-Separator character
	'[' [ '^' ] { character-range } ']'
	            character class (must be non-empty)
	c           matches character c (c != '*', '?', '\\', '[')
	'\\' c      matches character c

character-range:
	c           matches character c (c != '\\', '-', ']')
	'\\' c      matches character c
	lo '-' hi   matches character c for lo <= c <= hi
```

## Gotcha
`.earthlyignore` is currently applied only to local targets. If one is present in the context of a remote target, it is silently ignored and no exclusion happens.

## Prefer precise COPY
The best-practices page says `.earthlyignore` is best left as a last resort for tuning `COPY`: new irrelevant files would have to be added to the ignore file by hand, which is error-prone. It is safer to list the files a build needs in `COPY` commands, because a newly needed file that is missing usually makes the build fail visibly, whereas a new file that is missing from the ignore file is easy to overlook.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthfile/earthlyignore.md, guides/best-practices.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: removed the claim that a forgotten exclusion silently invalidates cache, which best-practices.md does not say. Only the .earthlyignore passage of best-practices.md (about lines 70 to 110) was read, not the whole page.

Method: documentation only; no commands were run.

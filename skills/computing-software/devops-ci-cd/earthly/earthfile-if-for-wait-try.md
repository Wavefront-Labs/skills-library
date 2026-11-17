---
id: computing-software.devops-ci-cd.earthly.earthfile-if-for-wait-try
name: earthfile-if-for-wait-try
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthfile, if, else, for, wait, try, finally, control-flow]
level: practitioner
status: docs-checked
description: "Control flow in Earthfiles: IF/ELSE IF/ELSE, FOR ... IN with --sep, WAIT blocks for ordering pushes and outputs, and the experimental TRY/FINALLY clause."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/earthfile.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IF, FOR, WAIT, TRY

## IF
```
IF [<condition-options>...] <condition>
  <if-block>
ELSE IF [<condition-options>...] <condition>
  <else-if-block>
ELSE
  <else-block>
END
```
The condition runs in the build environment; exit code zero runs the block. Typical use is POSIX `[ ... ]`:
```Dockerfile
IF [ -f ./foo ]
  EXPOSE 8080
END
```
Any command works, e.g. `IF ./semver-gt "$A" "$B"`. A condition needs a build environment, so a `FROM` (or `LOCALLY`) must come first. This is invalid because `IF` precedes any `FROM`:
```Dockerfile
ARG base=alpine
IF [ "$base" = "alpine" ]
    FROM alpine:3.18
```
Fix: add `FROM busybox` before the `IF`. Filesystem changes made inside conditions are not preserved. Options mirror RUN: `--privileged`, `--ssh`, `--no-cache`, `--mount <mount-spec>`, `--secret <env-var>=<secret-id>`.

## FOR
`FOR [<options>...] <variable-name> IN <expression> ... END`. The expression can be a constant list (`foo bar buz`), a command (`$(echo foo bar buz)`) or parameterized (`foo $BARBUZ`). `--sep <separator-list>` sets the tokenizer; default is tab, newline and space. The variable is set as a build arg in the block. Filesystem changes in the expression are not preserved. Same extra options as IF.
```Dockerfile
FOR dir IN $(ls -d */)
  BUILD "./$dir+build"
END
```

## WAIT
`WAIT ... END` runs the enclosed commands (in parallel with each other) and waits for them, including pushes and local outputs, before continuing.
```Dockerfile
WAIT
  BUILD +myimg
  BUILD +myotherimg
END
RUN --push ./deploy ...
```
```Dockerfile
RUN ./generate > data
WAIT
  SAVE ARTIFACT data AS LOCAL output/data
END
RUN ./test data # even if this fails, data will have been output
```

## TRY (experimental)
Needs `VERSION --try 0.8`. `TRY <try-block> FINALLY <finally-block> END` always runs the finally block. For now only a single `RUN` is allowed in the try block and only `SAVE ARTIFACT` commands in the finally block, e.g. to output `junit.xml`:
```Dockerfile
TRY
    RUN ./test.sh
FINALLY
    SAVE ARTIFACT junit.xml AS LOCAL ./
END
```

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: earthfile/earthfile.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.groovy.args-script-properties
name: args-script-properties
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, args-script-properties]
level: intro
status: draft
description: "Access args, System properties, environment variables and set exit codes in Groovy scripts."
sources:
  - https://docs.groovy-lang.org/latest/html/documentation/tools-groovy.html
  - https://docs.groovy-lang.org/latest/html/gapi/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Script arguments, environment and exit codes
- Scripts get `args` (String[]); `System.getenv('HOME')`, `System.properties['user.dir']`.
- Exit: `System.exit(2)` or `return` from a script; uncaught exceptions exit with 1 and print a stack trace.
- Read stdin: `System.in.eachLine { }` or `new Scanner(System.in)`.
- Print to stderr: `System.err.println 'x'` or `System.err << 'x'`.
- Fail fast on missing config: `assert args.size() >= 1 : 'usage: tool file'`.

## Gotchas
- `System.exit` skips `finally` blocks and shutdown ordering concerns for threads.
- Do not echo secrets from `System.getenv` into logs.

## Self-check
`groovy -e "println args" a b` prints `[a, b]`.

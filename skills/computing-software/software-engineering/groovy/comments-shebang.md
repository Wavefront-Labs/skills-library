---
id: computing-software.software-engineering.groovy.comments-shebang
name: comments-shebang
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, comments-shebang, groovy-lexical]
level: intro
status: docs-checked
description: "Groovy comment forms (line, block, Groovydoc) and the shebang line that lets a .groovy file run as a script."
sources:
  - https://groovy-lang.org/syntax.html
  - https://github.com/apache/groovy/blob/master/src/spec/doc/core-syntax.adoc
  - https://github.com/apache/groovy/blob/master/src/spec/doc/tools-groovy.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comments and shebang line
- Comments: `// line`, `/* block */`, `/** Groovydoc */`.
- A first line `#!/usr/bin/env groovy` is allowed (the `#` must be the first character of the file; indentation is a compilation error); make the file executable and run it directly.
- Run a script: `groovy Hello.groovy` or inline `groovy -e "println 1+1"`.

## Gotchas
- `/* */` comments do not nest.

## Self-check
Create a file with `#!/usr/bin/env groovy` and `println 'hi'`, run `groovy file.groovy`, confirm output.

## Checked

2026-11-02. Confirmed against the Syntax chapter (comments, Groovydoc, shebang line) and the groovy command page (-e, running a script). Removed: the groovydoc-tool claim and the shebang-elsewhere claim.

Method: documentation only; no commands were run.

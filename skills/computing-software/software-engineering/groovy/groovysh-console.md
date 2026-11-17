---
id: computing-software.software-engineering.groovy.groovysh-console
name: groovysh-console
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, groovysh-console]
level: intro
status: docs-checked
description: "Explore Groovy interactively with groovysh: variables, shared state, slash commands and the interpreter mode switch."
sources:
  - https://docs.groovy-lang.org/latest/html/documentation/tools-groovy.html
  - https://groovy-lang.org/groovysh.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# groovysh
`groovysh` is a REPL for evaluating expressions, defining classes and running small experiments. Line editing, history and completion come from JLine3.

- Commands start with a slash: `/help` lists them. Examples: `/load`, `/save`, `/imports`, `/show` (console variables), `/types`, `/methods`, `/del`, `/reset` (clear the buffer), `/clear` (clear the terminal), `/grab` (add Maven dependencies to the classpath), `/console` (launch the Groovy console), `/exit`.
- Useful options: `-q` (quiet), `-e <code>` (evaluate first, then stay interactive), `-cp` (must be the first argument), `-D name=value`.
- The result of the last evaluation is stored in `_`. After an exception, the message is printed and the shared variable `exception` is set.
- Each input runs in isolation. Imports, classes and methods are remembered; use shared variables to carry results.

## Variables: the main trap
- `foo = "bar"` (no `def`, no type) sets a shared variable that later inputs see.
- `def foo = "bar"` is a local variable and is forgotten after that input.
- Interpreter mode (`interpreterMode`, set with `/setopt`) lets typed and `def` variables be remembered. Check the groovysh page for the exact option syntax in your version.
- Methods defined in the shell are stored as closures in the shared variables when interpreter mode is off, so variables and methods share one namespace.

## Self-check
Start `groovysh`, enter `x = 2`, then `x * 21`, and confirm 42. Then enter `def y = 1` followed by `y` and confirm `y` is not found.

## Checked
Read the groovysh page (features, repl model, variables, methods, exceptions, command list) and the Groovy tools page. Removed: the colon-prefixed `:help` style (current commands use a slash), the `@Grab`-in-session claim, Windows terminal quirks, and the groovyConsole `Ctrl+R` and Inspect AST claims (not on pages read).

Method: docs-checked 2026-11-09 against the groovysh page and the Groovy tools documentation page.

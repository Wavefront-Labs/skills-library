---
id: computing-software.software-engineering.elixir.alias-import-require-use
name: alias-import-require-use
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, alias, import, require, use, __using__, directive, lexical-scope, alias-import-require, elixir-modules]
level: practitioner
status: docs-checked
description: "Use alias/import/require/use directives with lexical scope, import only what you need, and know that use calls the __using__ macro."
sources: ["https://hexdocs.pm/elixir/alias-require-and-import.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# alias, import, require and use

**Goal:** bring other modules into scope minimally and predictably.

```elixir
alias MyApp.Accounts.User              # then User.new
alias MyApp.Accounts.{User, Role}
alias MyApp.Billing, as: B
import Enum, only: [map: 2]
import List, except: [flatten: 1]
require Logger                         # needed to call macros like Logger.info/1
defmodule MyApp.Web do
  defmacro __using__(_opts) do
    quote do
      import Plug.Conn
      alias MyApp.Repo
    end
  end
end
use MyApp.Web                          # require MyApp.Web, then run MyApp.Web.__using__/1
```

## Rules
- Directives are lexically scoped: they apply from the line to the end of the enclosing module or function.
- `require` is needed for macros of another module (not for functions); `import` also requires.
- Prefer `alias` for readability; avoid blanket `import` (ambiguity errors when two imports define the same name/arity).

## Failure modes
- Importing the same function name and arity from two modules makes calls ambiguous: prefer `import ..., only:` or `alias`.

## Self-check
Why is `require Logger` needed before `Logger.info("x")`? Because `info/1` is a macro.

## Checked
2026-11-02: confirmed against Elixir guide "alias, require, import, and use" (lexical scope, require for macros, `only:`/`except:`, use and __using__). Removed: exact error messages and style advice on use.
Method: documentation only; no commands were run.

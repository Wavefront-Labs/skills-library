---
id: computing-software.software-engineering.haskell.ghci-workflow-and-commands
name: ghci-workflow-and-commands
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, ghci, repl, reload, ghci-type, ghci-info, ghci-kind, browse, ghci-conf, cabal-repl, load-interpreted, ghci-workflow-and-commands, haskell-debugging]
level: intro
status: docs-checked
description: "Use GHCi productively: :l, :r, :t, :i, :k, :browse, :set options, multiline input, .ghci files, cabal repl and -fobject-code."
sources: ["https://downloads.haskell.org/ghc/latest/docs/users_guide/ghci.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GHCi

**Goal:** a fast edit-reload-test loop.

```bash
ghci Main.hs            # or: cabal repl / stack ghci
```
```
ghci> :l Foo.hs            -- load        :r  reload        :m + Data.List  add module to scope
ghci> :t map               -- type        :t +d expr  default type variables
ghci> :i Maybe             -- info: definition, instances, location
ghci> :k Either            -- kind
ghci> :browse Data.Char    -- exports
ghci> :doc map             -- Haddock (if installed)
ghci> :set -Wall -XLambdaCase -fno-warn-type-defaults
ghci> :set prompt "λ> "
ghci> :{
ghci| f x = x + 1
ghci| :}                    -- multi-line block (or :set +m for layout-aware)
ghci> let y = 5             -- bindings persist
ghci> it                    -- the last expression's value
ghci> :main arg1 arg2       -- run main with args    :! ls shell
ghci> :q
```

## .ghci
GHCi reads `ghci.conf` from its app-data directory (usually `$HOME/.ghc` or `$XDG_CONFIG_HOME/ghc` on Unix) and then `./.ghci`. Sourcing an untrusted `./.ghci` is a security risk because it runs arbitrary commands; `:set local-config` inhibits it, and `-ignore-dot-ghci` skips startup files. In these files prefer `:seti` for language options.
Example `.ghci`:
```
:set -Wall -XOverloadedStrings
:set prompt "ghci> "
import qualified Data.Map as M
```

## Tips
- `:set +t` prints the type of results; `:set +s` timing and memory.
- `-fobject-code` (or `:set -fobject-code`) compiles instead of interpreting: faster execution but loses debugger/breakpoints on those modules; `:set -fbyte-code` to switch back.
- `-fdefer-type-errors` lets you load and run code with type errors until the bad expression is evaluated.
- `:script file` runs commands from a file. `cabal repl --repl-options=-fobject-code`.
- `ghcid` (a separate tool) re-runs `ghci` on save and shows compile errors continuously; HLS covers most of that use case.

## Gotchas
- Interpreted code is slow; benchmarks need compiled `-O2`.
- GHCi enables ExtendedDefaultRules and disables the monomorphism restriction, so some expressions behave differently from compiled code.
- Top-level `let` redefinitions shadow earlier ones.

## Self-check
- [ ] You trust every `./.ghci` you load.
- [ ] `:r` after saving shows the new behaviour.

## Checked

2026-11-02. Confirmed against the GHC User's Guide ghci page: :doc, :browse, :kind, :main, :script, :set +t/+s/+m, -fobject-code, -fbyte-code, startup files, ExtendedDefaultRules. Removed or fixed: unsupported .ghci permissions claim.
Method: documentation only; no commands were run.

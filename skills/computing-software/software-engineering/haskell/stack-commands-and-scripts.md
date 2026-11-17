---
id: computing-software.software-engineering.haskell.stack-commands-and-scripts
name: stack-commands-and-scripts
category: computing-software
field: software-engineering
product: haskell
tags: [haskell, stack-script, stack-exec, stack-install, stack-haddock, stack-ghci, stack-docker, stack-build-fast, stack-commands-and-scripts]
level: practitioner
status: docs-checked
description: "Everyday Stack commands (build flags, ghci, exec, install), single-file scripts with the stack script interpreter, and Docker and Nix integration."
sources: ["https://docs.haskellstack.org/en/stable/commands/", "https://docs.haskellstack.org/en/stable/topics/scripts/", "https://docs.haskellstack.org/en/stable/topics/docker_integration/", "https://docs.haskellstack.org/en/stable/topics/nix_integration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stack commands and scripts

**Goal:** the common Stack workflow beyond `stack build`.

```bash
stack build --fast --file-watch          # -O0 plus rebuild on change
stack build --pedantic                   # -Wall -Werror for local packages
stack test --ta '--match "Parser"'       # pass args to the test program (--test-arguments)
stack run -- --verbose
stack ghci                               # load all local packages
stack exec -- ghc-pkg list               # run a command with the Stack environment
stack install                            # copy executables to the local bin dir
stack haddock                            # synonym for stack build --haddock
```

## Scripts
```haskell
#!/usr/bin/env stack
-- stack script --snapshot lts-24.43 --package text
{-# LANGUAGE OverloadedStrings #-}
import qualified Data.Text.IO as T
main = T.putStrLn "hi"
```
Make the file executable with `chmod +x` and run it, or run `stack <file>`. The Stack interpreter options comment declares the snapshot and packages; `stack script` ignores any project-level `stack.yaml`. A snapshot must be given with `--snapshot` (`--resolver` is deprecated). Pick a current LTS from stackage.org.

## Docker and Nix
`stack.yaml` can contain a `docker:` section (`enable: true`, `image: ...`) to build inside a container; the docs describe Linux 64-bit as the Docker requirement. A `nix:` section (`enable: true`, `packages: [zlib]`) builds in a Nix shell.

## Gotchas
- Arguments to the program need `--`; arguments to Stack come first.
- `--fast` builds are not benchmarks.
- A script is interpreted unless you pass `--compile` (quick, unoptimised) or `--optimize`; compilation is done only if the executable is missing or older than the script.
- Do not mix `stack install` binaries with ghcup/cabal ones on `PATH` without checking `which`.

## Self-check
- [ ] `stack build --pedantic` (GHC options `-Wall` and `-Werror`) is clean.
- [ ] Scripts pin the snapshot.

## Checked
2026-11-03. Confirmed against the Stack docs (commands index, build, test, install, haddock, script, scripts topic, docker and nix integration, non-project config): `--fast`, `--file-watch`, `--pedantic` (-Wall and -Werror), `--ta`/`--test-arguments`, install and haddock as synonyms of build flags, `--snapshot` with `--resolver` deprecated, `--compile`/`--optimize`, chmod +x scripts, docker and nix `enable`/`image`/`packages` keys. Removed: `stack hoogle`, `stack upgrade`, `--open`, and the static-linking flags (not in the pages read).
Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.clojure.clj-kondo-configuration-and-ci
name: clj-kondo-configuration-and-ci
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, clj-kondo, lint, static-analysis, config-edn, hooks, lint-as, exit-codes, ignore, clj-kondo-lint]
level: practitioner
status: docs-checked
description: "Lint Clojure with clj-kondo: install, --lint, .clj-kondo/config.edn levels, lint-as, ignore syntax, config-in-ns, importing library configs, exit codes for CI."
sources: ["https://github.com/clj-kondo/clj-kondo", "https://raw.githubusercontent.com/clj-kondo/clj-kondo/master/doc/config.md", "https://raw.githubusercontent.com/clj-kondo/clj-kondo/master/doc/install.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# clj-kondo

**Goal:** catch errors early without loading code.

```bash
clj-kondo --lint src test                       # file, directory or classpath; "-" reads stdin
clj-kondo --lint "$(clojure -Spath)" --copy-configs --skip-lint     # import library configs into .clj-kondo
clj-kondo --lint "$(clojure -Spath)" --dependencies --parallel      # populate the cache
clj-kondo --lint src --fail-level error         # warnings no longer give a non-zero exit
```
`.clj-kondo/config.edn`:
```clojure
{:linters {:missing-docstring {:level :warning}
           :unresolved-symbol {:level :off}}
 :lint-as {foo/my-defn clojure.core/defn
           foo/my-def  clj-kondo.lint-as/def-catch-all}
 :skip-comments true
 :config-in-ns {my.namespace {:linters {:unresolved-symbol {:level :off}}}}}
```
- Levels include `:off`, `:info`, `:warning`, `:error`; some linters are off by default (`:missing-docstring`,
  `:refer`, `:unused-value`).
- Exit codes: 0 no findings, 2 warnings found, 3 errors found; `--fail-level` controls the threshold.
- Ignore: `#_:clj-kondo/ignore` before a form; `#_{:clj-kondo/ignore [:invalid-arity]}` for specific linters;
  `{:clj-kondo/ignore [...]}` metadata on a namespace or macro.
- `:lint-as` lints a custom macro like a built-in; `def-catch-all` is for def/defn-like macros with no close
  match. Hooks (`:analyze-call`, `:macroexpand`) are documented in hooks.md.
- Config sources merge in order (later wins): `~/.config/clj-kondo/config.edn`, `:config-paths`, project
  `.clj-kondo/config.edn`, `CLJ_KONDO_EXTRA_CONFIG_DIR`, command line `--config`, then ns-local
  `:clj-kondo/config` metadata. `^:replace` replaces instead of merging.
- `--copy-configs` needs an existing `.clj-kondo` dir; configs land in `.clj-kondo/clj-kondo/<library>` and
  are meant to be committed. Commit everything under `.clj-kondo` except the cache dir (add `.cache` to
  `.gitignore`).
- Install: release binaries, an install script (macOS/Linux), `brew install borkdude/brew/clj-kondo`, scoop on
  Windows, ASDF, Linux packages, or run on the JVM or Docker.
- Editor support is via editor integration docs; clojure-lsp is not covered by the pages read.

## Self-check
Introduce an unused binding and an arity error and confirm both are reported with file and line.

## Checked
Method: 2026-11-08 read the clj-kondo README, doc/config.md and doc/install.md. Removed unsupported claims: `--config '{:output {:format :json}}'`, `:unused-binding`/`:unused-namespace` level examples, `:unresolved-symbol :exclude` syntax, `:hooks` config sample, the deps.edn install route, and the clojure-lsp embedding claim. Unchanged: self-check.

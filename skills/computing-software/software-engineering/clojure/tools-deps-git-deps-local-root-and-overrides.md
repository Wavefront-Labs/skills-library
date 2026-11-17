---
id: computing-software.software-engineering.clojure.tools-deps-git-deps-local-root-and-overrides
name: tools-deps-git-deps-local-root-and-overrides
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, tools-deps, git-deps, local-root, deps-gitlibs, override-deps, extra-deps, exclusions, sha, tag, tools-deps-git-local-aliases]
level: advanced
status: docs-checked
description: "Depend on git repos with :git/sha, local checkouts with :local/root, exclude and override transitive versions, and use :deps/prep-lib and gitlibs cache."
sources: ["https://clojure.org/reference/deps_and_cli", "https://clojure.org/reference/deps_edn"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Git deps, local roots, overrides

**Goal:** consume code that is not on Maven and resolve conflicts.

```clojure
{:deps
 {io.github.user/lib   {:git/tag "v1.0.0" :git/sha "<sha prefix>"}   ; :git/url inferred for io.github.*
  com.example/other    {:git/url "https://example.com/other.git" :git/sha "<full 40-char sha>"}
  my/local-lib         {:local/root "../local-lib"}
  org.clojure/tools.logging {:mvn/version "<current>" :exclusions [org.slf4j/slf4j-api]}}
 :aliases
 {:pin {:override-deps {org.clojure/core.async {:mvn/version "<version>"}}}}}   ; also :replace-deps, :extra-deps, :default-deps
```
- Git deps are checked out under `~/.gitlibs`, one working tree per sha. Branch names are not supported: `:git/sha` is required, and must be a full 40-char sha unless `:git/tag` is given, in which case a prefix works if both resolve to the same commit.
- `:git/url` is inferred from `io.github.ORG/PROJECT` (and `com.github.`, `io.gitlab.`, `io.bitbucket.` and other documented prefixes); https repos are accessed anonymously, ssh repos use your ssh identity.
- `:local/root` is required for local deps and points to a project directory or a jar, absolute or relative; a jar's `pom.xml`, if present, supplies its transitive deps.
- A library that needs build prep (compiling Java, etc.) declares `:deps/prep-lib` in its deps.edn; run
  `clojure -X:deps prep` to execute it.
- Version conflict rule: generally the newest version of a library is selected, but top-level dependency versions are always used unmodified, so pin a version by listing it in top-level `:deps` (or `:override-deps`). Two git shas are resolved to the descendant one; shas on parallel branches are an error.
  Use `clojure -Stree` to inspect which was selected.
- Related commands: `clojure -X:deps find-versions :lib group/artifact` lists available versions, `clojure -X:deps tree` prints the tree.

## Failure modes
- Classpath construction fails with "The following libs must be prepared before use" until `clojure -X:deps prep` has run for a lib that declares `:deps/prep-lib`.
- A tag whose commit differs from the given sha prefix is rejected (they must unpeel to the same commit).

## Self-check
Pin a transitive dep with `:override-deps` and confirm `clojure -Stree` reflects it.

## Checked
2026-11-03. Confirmed against the clojure.org deps.edn reference, Clojure CLI reference and Deps and CLI guide: git coord attributes and sha/tag rules, inferred git urls, ~/.gitlibs, :local/root, :exclusions, :override-deps, :default-deps, :replace-deps, :deps/prep-lib, `clojure -X:deps prep`, find-versions and tree, version selection rule. Removed: the "nearest-to-root" resolver claim (the docs say newest wins, top-level deps unmodified), the "changes picked up without install" remark, the `Manifest type not detected` message and the clone-error remark.
Method: documentation only; no commands were run.

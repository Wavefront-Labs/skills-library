---
id: computing-software.software-engineering.clojure.release-builds-versioning-and-reproducibility
name: release-builds-versioning-and-reproducibility
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, release, versioning, git-sha, reproducible-builds, ci, github-actions, artifacts, clojars, deploy-uberjar-checks]
level: practitioner
status: docs-checked
description: "Produce release artifacts in CI: version from git, run tests and lint first, build the uberjar, tag, and publish libraries to Clojars with deps-deploy."
sources: ["https://clojure.org/guides/tools_build", "https://github.com/slipset/deps-deploy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Release builds and CI

**Goal:** the same commands locally and in CI produce a trustworthy artifact.

CI steps (any runner; install a JDK and the Clojure CLI, then run the same commands you run locally):
```bash
clojure -M:test            # your own test alias
clojure -T:build uber      # application: compiled uberjar
clojure -T:build jar       # library: source jar
```
- Keep the build in a `build.clj` program run as a tool (`clojure -T:build <fn>`), with a `:build` alias that adds
  `io.github.clojure/tools.build` by `:git/tag` and `:git/sha` (tools.build guide). Then it runs the same locally and in CI.
- Derive the version from git: the guide shows `(def version (format "1.2.%s" (b/git-count-revs nil)))` for an
  ever-increasing commit count as the third component.
- Applications: the main namespace needs `(:gen-class)` and a `-main`; `b/compile-clj` then `b/uber` produce
  `target/<lib>-<version>-standalone.jar`, run with `java -jar`.
- Libraries: `b/write-pom`, `b/copy-dir`, `b/jar`, then deploy with `deps-deploy`: a `:deploy` alias with
  `:exec-fn deps-deploy.deps-deploy/deploy` and `:exec-args {:installer :remote :sign-releases? true :artifact "<jar>"}`,
  run as `clj -X:deploy`. It needs a `pom.xml` and reads `CLOJARS_USERNAME` and `CLOJARS_PASSWORD`; Clojars no
  longer accepts passwords for deploys, so put a Clojars token in `CLOJARS_PASSWORD` (store it in CI secrets).
- `:sign-releases? true` signs with your default GPG key; set `:sign-key-id` to use another.
- Pin tool versions (Clojure CLI, JDK) in CI; unpinned `latest` makes builds drift.

## Failure modes
- Passing locally but failing in CI due to an un-pinned Java or Clojure CLI version.
- Committing built jars; use release assets instead.
- Compile misses a dynamically loaded namespace: `compile-clj` compiles transitively but you may need to list extra
  namespaces.

## Self-check
Run the whole CI sequence locally from a clean clone; it must succeed without extra setup.

## Checked
2026-11-08. Confirmed: clojure.org tools.build guide (`-T:build` alias with git tag/sha, `build.clj`, jar and uberjar task sequences, `(:gen-class)` and `-main`, `git-count-revs`, standalone jar naming, transitive compilation); deps-deploy README (`:deploy` alias, `:exec-fn`, `:sign-releases?`, `:sign-key-id`, pom.xml requirement, `CLOJARS_USERNAME`/`CLOJARS_PASSWORD`, Clojars tokens). Removed: the GitHub Actions YAML and setup-clojure action, clj-kondo lint step, `git rev-parse HEAD` embedding, `~/.m2` cache advice and the `.clj-kondo` cache failure mode.
Method: documentation only; no commands were run.

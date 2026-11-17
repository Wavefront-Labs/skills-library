---
id: computing-software.software-engineering.clojure.dependency-scanning-and-supply-chain-hygiene
name: dependency-scanning-and-supply-chain-hygiene
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, security, dependencies, supply-chain, nvd, nvd-clojure, dependabot, antq, pinned-versions, clojars, security-dependencies]
level: practitioner
status: docs-checked
description: "Keep dependencies safe and current: scan with nvd-clojure, list outdated deps with antq, pin versions and SHAs, and review git/maven coordinates."
sources: ["https://github.com/rm-hull/nvd-clojure", "https://github.com/clj-commons/antq", "https://clojure.org/guides/deps_and_cli"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dependency and supply-chain security

**Goal:** know what you ship and fix known vulnerabilities.

```bash
# antq as a tool (Clojure CLI 1.11.1.1139 or later)
clojure -Ttools install-latest :lib com.github.liquidz/antq :as antq
clojure -Tantq outdated                    # report outdated deps
clojure -Tantq outdated :upgrade true      # upgrade interactively
clojure -Stree                              # full tree, spot unexpected transitive deps
```
- antq reads deps.edn, project.clj, shadow-cljs.edn, pom.xml, bb.edn, GitHub Actions workflows and more; Gradle is
  opt-in via `--check-gradle` and does not support `--upgrade`. `--transitive` scans transitive deps (default depth 5).
- `nvd-clojure` checks every jar on the classpath you pass it against the NVD database through OWASP DependencyCheck.
  Put it in a separate helper project, not in the project being analysed, and pass a production-like classpath
  (no dev/test tooling), for example from `clojure -Spath`. Follow the README for the exact command.
- nvd-clojure needs an NVD API key (`:nvd-api {:key ...}` in its edn config, or the `NVD_API_TOKEN` environment
  variable). The first run downloads the databases and can take ten minutes or more.
- By default the check exits abnormally if any vulnerability scores above 0 (`:fail-threshold`), which fails CI.
- Pin versions; prefer exact versions over ranges. For git deps pin the full `:git/sha`.
- Review new dependencies: maintainer, last release, open security issues; prefer fewer deps.
- Transitive overrides: `:override-deps` in an alias forces a version (shown in the deps_and_cli guide).
- Keep the JDK updated (security fixes) and base images rebuilt regularly.

## Failure modes
- Vulnerable transitive Java libraries (log libraries, serialisers, XML parsers) hidden deep in the tree.
- Using unmaintained forks pinned by SHA with no updates.
- Scanning a classpath that includes dev tooling, which reports findings you do not ship (or hides ones you do).

## Self-check
Run the dependency tree and list every direct dep with its last release date.

## Checked
2026-11-08. Confirmed: nvd-clojure README (separate helper project, production-like classpath, `-Spath`, API key via `:nvd-api :key` or `NVD_API_TOKEN`, ten-minute first run, `:fail-threshold` default 0, `-Stree` for the tree); antq README (supported files, tool install and `-Tantq outdated`, `:upgrade true`, `--check-gradle`, `--transitive` depth 5); clojure.org deps_and_cli guide (`:git/sha`, `:override-deps`). Removed: the incorrect alias comment on the antq command, Dependabot/Renovate support claim, Clojars token and 2FA advice, and the `:exclusions` tip (not shown in the pages read).
Method: documentation only; no commands were run.

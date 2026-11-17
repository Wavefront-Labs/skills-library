---
id: computing-software.software-engineering.clojure.configuration-aero-env-vars-and-secrets
name: configuration-aero-env-vars-and-secrets
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, config, aero, environment-variables, edn-config, profiles, secrets, 12-factor, system-getenv, config-aero-env]
level: practitioner
status: docs-checked
description: "Load layered configuration with Aero (#env, #profile, #or) validate it at startup, and keep secrets out of the repo."
sources: ["https://github.com/juxt/aero"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Configuration

**Goal:** typed, validated, environment-specific config.

`resources/config.edn`:
```clojure
{:server {:port #long #or [#env PORT 3000]}
 :db     {:url #env DATABASE_URL
          :pool-size #profile {:default 5 :prod 20}}
 :secrets #include #join [#env HOME "/.secrets.edn"]}
```
```clojure
(require '[aero.core :as aero])
(def cfg (aero/read-config (io/resource "config.edn") {:profile :prod}))
```
- Aero tags: `#env`, `#envf`, `#or`, `#join`, `#profile` (a map with a `:default` entry), `#long`, `#double`,
  `#boolean`, `#keyword`, `#include`, `#merge`, `#ref` (a `get-in` path), `#hostname`, `#user`. `#profile` replaces
  the deprecated `#cond`.
- Use `io/resource` with `read-config`: a plain file path works in the REPL but can fail from an uberjar.
  `#include` resolves relative to the config file by default (not inside jars); pass `:resolver` (for example
  `resource-resolver`) to change that.
- Aero's README calls environment variables for passwords and other confidential information bad practice (the
  process environment is easy to leak) and recommends `#include` of a separate secrets file.
- Aero integrates with Plumatic Schema for validating the data returned by `read-config`; validate at startup and
  fail fast.
- Keep config as data and pass it into components rather than reading env throughout the code.

## Failure modes
- Missing env var yields nil and a later NullPointerException; validate early.
- Different profiles drifting; test the production profile's shape in CI.

## Self-check
Start with `PORT` unset and set; verify the port, and that a missing required var fails at startup.

## Checked
2026-11-08. Partial read of the Aero README (searched tags and read the relevant sections). Confirmed: `read-config` with `io/resource` and `{:profile ...}`, `#env`, `#envf`, `#or`, `#join`, `#profile`/`:default`, `#long`, `#boolean`, `#keyword`, `#double`, `#include` and `#ref`, resolver behaviour, the environment-variables-for-secrets warning, Plumatic Schema integration. Removed: `#int`, `System/getenv` and `-D` system property alternatives, spec/malli validation claim, and the `#env API_KEY` example, none of which the README states.
Method: documentation only; no commands were run.

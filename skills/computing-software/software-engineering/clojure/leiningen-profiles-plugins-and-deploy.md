---
id: computing-software.software-engineering.clojure.leiningen-profiles-plugins-and-deploy
name: leiningen-profiles-plugins-and-deploy
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, leiningen, profiles, plugins, with-profile, lein-ancient, lein-kibit, lein-cloverage, deploy, release, middleware, lein-profiles-plugins]
level: advanced
status: draft
description: "Use Leiningen profiles (:dev, :test, :uberjar, merge and composite), user-level plugins, with-profile / pprint, and deploy to Clojars with lein deploy."
sources: ["https://leiningen.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Leiningen profiles, plugins, deploy

**Goal:** vary builds across environments and publish libraries.

```clojure
:profiles {:dev  [:project/dev :profiles/dev]       ; composite, merging a local, uncommitted profile
           :project/dev {:dependencies [[ring/ring-mock "<v>"]]}
           :test {:resource-paths ["test-resources"]}
           :ci   {:jvm-opts ["-Xmx512m"]}}
:plugins [[lein-cloverage "<v>"] [com.github.clj-kondo/lein-clj-kondo "<v>"]]
:deploy-repositories [["clojars" {:url "https://repo.clojars.org"
                                  :username :env/clojars_username
                                  :password :env/clojars_token
                                  :sign-releases false}]]
```
```bash
lein with-profile +ci test         # add a profile to the defaults; `-dev` removes one
lein with-profile base,ci test     # replace the active set
lein pprint                        # show the merged project map
lein show-profiles
lein deploy clojars                # publish a jar built from the current version (no -SNAPSHOT for releases)
```
- Profile vectors compose: a profile may be a map or a vector of other profile names.
- `~/.lein/profiles.clj` `:user` profile applies to every project (put cider-nrepl, kibit here, not in project.clj).
- Metadata `^:replace` or `^:displace` on a value controls merge behaviour (replace instead of concatenate).
- Read credentials from the environment via `:env/...` keys in `:deploy-repositories`; never commit them.

## Failure modes
- Dev dependencies leaking into the uberjar by editing top-level `:dependencies` instead of `:dev`.
- Plugin version mismatch with the Leiningen version.

## Self-check
`lein pprint` under two different `with-profile` options shows different `:dependencies`.

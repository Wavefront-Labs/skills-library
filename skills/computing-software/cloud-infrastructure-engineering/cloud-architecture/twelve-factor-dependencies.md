---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.twelve-factor-dependencies
name: twelve-factor-dependencies
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, twelve-factor, 12-factor-app, twelve-factor-dependencies, dependency-declaration, lockfiles, dependency-isolation, container-images, system-tools]
level: practitioner
status: docs-checked
description: "Apply factor II: declare every dependency in a manifest, isolate them from the host with a dependency isolation tool, and vendor any system tool the app shells out to."
sources: ["https://12factor.net/dependencies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Factor II: explicitly declare and isolate dependencies

**Rule:** a twelve-factor app never relies on the implicit existence of system-wide packages. It declares all
dependencies, completely and exactly, in a manifest, and uses a dependency isolation tool at run time so
nothing leaks in from the surrounding system. Declaration and isolation must be used together; either alone
is not sufficient. The same specification applies to production and development.

## Examples from the factor page
| Ecosystem | Declare | Isolate |
|---|---|---|
| Ruby | Bundler `Gemfile` | `bundle exec` |
| Python | Pip | Virtualenv |
| C | Autoconf | static linking |

Setup command examples on the page: `bundle install` (Ruby/Bundler), `lein deps` (Clojure/Leiningen). A new
developer should need only the language runtime and dependency manager, then one deterministic build command.
Apply the same idea in your own ecosystem: find its manifest and its isolation mechanism.

## System tools
Shelling out to ImageMagick or curl relies on a tool that may be missing, or a different incompatible
version, on a future system. The page says such a tool should be vendored into the app.

## Steps
1. Build from the manifest only on a clean machine or container; anything that breaks was implicit.
2. Use one documented command for a fresh clone to build and run.
3. Treat every system tool the code invokes as a dependency to vendor or install explicitly.

## Verify
- [ ] A fresh clone plus the one documented command builds and runs.
- [ ] No code path shells out to a tool that is not vendored or installed by the build.

## Checked
2026-11-01. Confirmed against the 12factor.net Dependencies page. Removed: the Node, Java, Go and .NET
lockfile commands, the Python lockfile tools, base-image digest pinning, Renovate/Dependabot and the CI
lockfile-sync rule, which the page does not state and which were not verified against tool documentation.
Method: documentation only; no commands were run.

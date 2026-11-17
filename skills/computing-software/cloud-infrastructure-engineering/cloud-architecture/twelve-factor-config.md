---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.twelve-factor-config
name: twelve-factor-config
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, twelve-factor, 12-factor-app, twelve-factor-config, environment-variables, config-in-environment, secrets-injection, config-validation, config-groups]
level: practitioner
status: docs-checked
description: "Apply factor III: keep deploy-varying config out of code in environment variables, avoid named environment config groups, validate at startup, use Kubernetes env."
sources: ["https://12factor.net/config", "https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Factor III — Store config in the environment

**Config** = everything that varies between deploys: resource handles (DB URLs), credentials,
per-deploy values (hostnames, feature toggles). Not config: internal wiring (routes, DI), which
belongs in code.

**Litmus test (12factor.net):** could you open-source the codebase right now without leaking a credential?

## Steps
1. Grep for hard-coded hosts, keys, `if env == "prod"` branches; move values to env vars.
   12factor.net: env vars are easy to change between deploys without code changes, are unlikely
   to be checked into the repo by accident (unlike config files), and are a language- and
   OS-agnostic standard.
2. **Avoid environment-named config groups** (`config/prod.yml`, `config/staging.yml`). In
   12factor, env vars are granular controls, orthogonal to each other, never grouped as
   "environments" but managed independently per deploy; this scales as deploys multiply.
3. **Validate at startup** with a typed settings object in your framework of choice; fail fast
   with a clear message listing missing or invalid keys (project practice, not from the cited pages).
4. Kubernetes: set container env vars with `env` (a value per named variable) or `envFrom`
   (all key-value pairs of a referenced ConfigMap or Secret, with an optional common prefix).
   Keep secrets out of images and the codebase.
5. Document every variable (name, purpose, default, required) in one place.

## Gotchas
- Strict separation: constants in code that vary between deploys violate factor III.
- Internal application config that does not vary between deploys (routes, how modules are
  wired) is best kept in code.
- Env vars are fixed when the container starts; changing them means a new Pod/deploy.

## Verify
- [ ] The codebase could be open-sourced now without exposing a credential.
- [ ] Image is identical across environments; only env differs.
- [ ] Missing required variable makes the process exit non-zero at boot with the variable name.

## Checked
2026-11-08
Method: documentation only; no commands were run.
Confirmed against 12factor.net Config and the Kubernetes Define Environment Variables for a Container task page. Removed unconfirmed claims: named validation libraries, secrets-manager injection mechanisms per cloud, env var leakage vectors, and the JSON-blob advice.

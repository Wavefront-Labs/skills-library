---
id: computing-software.devops-ci-cd.release-engineering.environment-configuration-build-once-configure-per-env
name: environment-configuration-build-once-configure-per-env
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, environment-configuration, externalised-config, config-injection, twelve-factor-config, build-once-deploy-many, configuration-management, config-per-environment, environment-variables, configmap, helm-values-per-env, kustomize-overlays, config-schema, config-validation, startup-validation, feature-flags-vs-config, secrets-vs-config, config-drift, config-as-code, environment-parity, runtime-config, config-versioning, dotenv]
level: practitioner
status: draft
description: "Keep one artifact for every environment: externalise config (env vars, mounted files, config service), per-env overlays, startup validation against a schema, secrets separate from settings."
sources: ["Humble & Farley, Continuous Delivery (2010), ch. 2 Configuration Management", "https://12factor.net/config", "https://kubernetes.io/docs/concepts/configuration/configmap/", "https://kustomize.io/", "https://helm.sh/docs/chart_template_guide/values_files/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Environment configuration: build once, configure per environment

**Goal:** the image that passed staging is byte-for-byte what runs in production; only
the configuration it is given differs — and that configuration is versioned, validated and
reviewable.

## 1. The rule and its consequences
Build once (CD ch. 2 and 5): no `-Denv=prod` compile flags, no `npm run build:prod`
producing a different bundle, no environment-specific Docker tags built from source. If
the frontend bakes `API_URL` at build time, inject it at *serve* time instead
(`window.__CONFIG__` from a templated `config.js`, or `envsubst` in the container
entrypoint). Everything that differs between environments is **data read at startup or
runtime**.

## 2. Where config comes from (12-factor, refined)
| mechanism | good for | notes |
|---|---|---|
| **Environment variables** | small scalar settings; secrets injected by the platform | flat namespace; no types; visible in `/proc` and crash dumps — fine for settings, careful with secrets |
| **Mounted files** (ConfigMap/Secret volumes, `/etc/app/config.yaml`) | structured config, certificates, large values | hot-reloadable (watch the file); supports schema validation |
| **Config service / parameter store** (AWS SSM/AppConfig, Consul, Spring Cloud Config) | dynamic settings, many services | adds a runtime dependency — cache and fail safe with last-known-good |
| **Feature flags** (LaunchDarkly/OpenFeature) | behaviour toggles changed *without* deploy | not for connection strings; flags have lifecycle and cleanup |
| **CLI args / defaults in code** | developer defaults | production must not rely on them |
Precedence: defaults in code < config file < env vars < explicit CLI (document it; most
libraries — Viper, Pydantic Settings, Spring, node-config — implement this order).

## 3. Repo layout for per-env config
```
deploy/
  base/            # Kustomize base or Helm chart: everything common
  envs/
    dev/           values.yaml | kustomization.yaml + configmap patch
    staging/
    prod/
```
Keep the **delta** per env tiny and reviewable: replica counts, resource limits, URLs,
feature defaults. If a prod overlay grows past a screen, something belongs in base with
a sane default. Generate the ConfigMap from a file (`configMapGenerator` with a hash
suffix → pods roll when config changes; Helm `checksum/config` annotation does the same).
Environment names are config too: avoid `if env == "prod"` branches in code; expose the
*behaviour* as a setting (`PAYMENTS_LIVE_MODE=true`) so a "prod-like" test env can flip it.

## 4. Secrets are not settings
Settings (URLs, limits, toggles) live in Git in plain text. Secrets (passwords, keys)
come from a secret store at deploy/run time (External Secrets Operator, Vault Agent,
cloud secret managers, SOPS-encrypted files) and are mounted or injected — never
committed, never in the same ConfigMap. Reference secrets *by name* in settings
(`DB_PASSWORD_SECRET=prod/db/app`) when the app fetches them itself.

## 5. Validate at startup, fail fast
Define a schema for the whole config (Pydantic/`zod`/JSON Schema/Go struct + validator)
and fail on boot with a precise message if anything is missing, mistyped or
inconsistent (`DATABASE_URL` missing; `CACHE_TTL` not an int; `TLS_CERT` set but `TLS_KEY`
not). A pod that crash-loops on bad config is far better than one that starts and
silently uses a default. Print the **effective config** (secrets redacted) at startup
and expose it at `/debug/config` (auth-gated) — the first thing you'll want in an
incident. Validate the *rendered* config in CI too: `helm template` + `kubeconform` +
a custom check that every `envs/*` sets the required keys (a tiny script or `conftest`).

## 6. Hot reload or restart?
Restart-on-change is simpler and safer (rolling update, health checks gate it). Hot
reload only for values that must change without a rollout (log level, rate limits,
flags) — and then via a mechanism designed for it (flag SDK, `SIGHUP` + file watch with
atomic swap). Mixed models cause "it changed in the file but not in the process" tickets.

## 7. Versioning and drift
- Config repo (or `deploy/` dir) is tagged alongside releases; a deployment = (artifact
  version, config version) — record both in the deployment event.
- Drift: compare live ConfigMaps/env against Git regularly (Argo CD/Flux do it for
  Kubernetes; for VMs, `ansible --check` or a nightly diff job). Manual `kubectl edit` of
  prod config is reverted by GitOps — make that policy explicit.
- Rollback of a bad config change is a Git revert + sync; keep config changes in their
  own commits so reverting one doesn't revert the image bump.
- Diff environments routinely (`diff <(yq envs/staging) <(yq envs/prod)`) — unexpected
  differences are tomorrow's "works in staging" bug.

## Verify
- [ ] The prod deployment references the same image digest that passed staging.
- [ ] Removing a required setting makes the service exit non-zero at startup with a clear message.
- [ ] `git grep -i password deploy/` finds only secret *references*, never values.
- [ ] Per-env overlays are under ~50 lines each and the staging↔prod diff is explainable line by line.

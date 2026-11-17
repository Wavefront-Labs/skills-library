---
id: computing-software.devops-ci-cd.release-engineering.config-reload-without-redeploy
name: config-reload-without-redeploy
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, config-reload, sighup, hot-reload, configmap-reload, reloader, dynamic-configuration]
level: practitioner
status: docs-checked
description: "Apply configuration changes without redeploying: SIGHUP and reload endpoints, ConfigMap update semantics, Reloader and checksum annotations, validation."
sources:
  - https://kubernetes.io/docs/concepts/configuration/configmap/#mounted-configmaps-are-updated-automatically
  - https://github.com/stakater/Reloader
  - https://helm.sh/docs/howto/charts_tips_and_tricks/#automatically-roll-deployments
  - https://nginx.org/en/docs/control.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Config reload without redeploy

Two strategies: **hot reload** inside the running process, or **automatic rolling restart** when config changes. Both avoid a new build.

## Process-level reload
| Software | Reload |
|---|---|
| nginx | `nginx -s reload` (equivalent to SIGHUP: reload the configuration) |
| Prometheus | `POST /-/reload` (with `--web.enable-lifecycle`) or SIGHUP |
Rules: validate with the software's own config check before reload, and make the app keep the old config if the new one fails to parse.

For your own services:
- Handle SIGHUP or watch the file, using your framework's reload support.
- Swap config atomically (build new config object, validate, then replace a pointer); never mutate fields in place mid-request.
- Expose the active config version/hash in metrics or `/info`.

## Kubernetes ConfigMaps
- Mounted as a **volume**: files are updated eventually, within the kubelet sync period plus the cache propagation delay.
- **subPath** mounts do not receive ConfigMap updates, and ConfigMaps consumed as **environment variables** are not updated automatically: the pod must restart.
- Immutable ConfigMaps (`immutable: true`) never change; create a new name per version.

Restart-on-change options:
```yaml
# Helm: checksum annotation rolls the Deployment whenever the rendered config changes
spec:
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
```
```yaml
# Stakater Reloader: watches referenced ConfigMaps/Secrets and triggers a rollout
metadata:
  annotations:
    reloader.stakater.com/auto: "true"
```

## Choosing
- Frequent, low-risk tuning: hot reload or a config store with in-process refresh.
- Structural config (ports, DB URLs, feature wiring): rolling restart through the normal rollout machinery, which already has health checks and rollback.

## Verify
- [ ] Changing config updates behaviour within the expected time without a new image; active config hash visible.
- [ ] An invalid config is rejected and the service keeps serving with the previous one.

## Checked

2026-10-28. Confirmed: nginx control page (HUP signal for changing configuration, `-s` signals); Prometheus management API (`/-/reload`, `--web.enable-lifecycle`, SIGHUP); Kubernetes ConfigMap page (volume updates take up to the kubelet sync period plus cache propagation delay, environment variables are not updated automatically, subPath mounts do not receive updates, immutable ConfigMaps); Helm tips page (`checksum/config` annotation with `sha256sum`); Reloader README (`reloader.stakater.com/auto`). Removed: HAProxy, PostgreSQL, Envoy and Alertmanager rows, validator command names, framework reload examples, the `..data` symlink detail, the Kustomize hash claim and the named config stores.

Method: documentation only; no commands were run.

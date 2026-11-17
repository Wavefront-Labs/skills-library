---
id: computing-software.devops-ci-cd.argo-cd.migrating-argocd-cm-plugins-to-sidecars
name: migrating-argocd-cm-plugins-to-sidecars
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, cmp-migration, config-management-plugin, cmp-sidecar]
level: practitioner
status: docs-checked
description: "Move legacy configManagementPlugins in argocd-cm to sidecar CMPs (removed in Argo CD 2.8): plugin.yaml conversion, repo-server patch and Application spec changes."
sources: ["https://argo-cd.readthedocs.io/en/stable/operator-manual/config-management-plugins/#migrating-from-argocd-cm-plugins", "https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/2.7-2.8/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating argocd-cm plugins to sidecars

`configManagementPlugins` in `argocd-cm` was removed in 2.8.

## Convert
Old:
```yaml
configManagementPlugins: |
  - name: kustomize-envsubst
    generate:
      command: [sh, -c]
      args: ["kustomize build . | envsubst"]
```
New `plugin.yaml` (ConfigMap mounted into a sidecar):
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ConfigManagementPlugin
metadata: { name: kustomize-envsubst }
spec:
  version: v1.0
  generate:
    command: [sh, -c]
    args: ["kustomize build . | envsubst"]
```
Repo-server patch (`<argocd-home>` is the argocd user home directory in the Argo CD image):
```yaml
containers:
  - name: kustomize-envsubst
    image: registry.example.com/cmp-kustomize-envsubst:1.0   # must contain kustomize + envsubst
    command: [/var/run/argocd/argocd-cmp-server]
    securityContext: { runAsNonRoot: true, runAsUser: 999 }
    volumeMounts:
      - { name: var-files, mountPath: /var/run/argocd }
      - { name: plugins, mountPath: <argocd-home>/cmp-server/plugins }
      - { name: cmp-plugin, mountPath: <argocd-home>/cmp-server/config/plugin.yaml, subPath: plugin.yaml }
```

## Application change
With `version` set, the plugin name becomes `kustomize-envsubst-v1.0`:
```yaml
source:
  plugin:
    name: kustomize-envsubst-v1.0       # or omit name and use discover rules
    env: [{ name: FOO, value: bar }]    # exposed to the plugin as ARGOCD_ENV_FOO
```
Environment variables are now prefixed `ARGOCD_ENV_`; update scripts accordingly.

## Verify
- [ ] The sidecar starts and the app renders without errors.

## Checked
2026-10-28. Confirmed on the 2.7 to 2.8 upgrade page: plugins installed via the `argocd-cm` ConfigMap do not work from v2.8. Confirmed on the config management plugins page: sidecar with `argocd-cmp-server` entrypoint (`/var/run/argocd/argocd-cmp-server`), `runAsNonRoot` with `runAsUser: 999`, `var-files` and `plugins` volume mounts, plugin file location `cmp-server/config/plugin.yaml` in the sidecar, plugin name `<plugin name>-<plugin version>` when `version` is set, `ARGOCD_ENV_` prefix for env vars.
Removed (not confirmed): the exact error messages and sidecar log line, the `/tmp` volume mount.

Method: documentation only; no commands were run.

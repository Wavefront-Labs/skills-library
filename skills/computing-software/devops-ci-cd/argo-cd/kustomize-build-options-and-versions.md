---
id: computing-software.devops-ci-cd.argo-cd.kustomize-build-options-and-versions
name: kustomize-build-options-and-versions
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, kustomize-build-options, kustomize-version, load-restrictor, custom-kustomize-binary]
level: advanced
status: docs-checked
description: "Configure how Argo CD runs kustomize: global kustomize.buildOptions, load restrictor, multiple kustomize binary versions selected per application, and installing them."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/kustomize/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/custom_tools/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/argocd-cm-yaml/", "https://github.com/kubernetes-sigs/kustomize/blob/master/kustomize/commands/build/flagloadrestrictor.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kustomize build options and versions

## 1. Build options (argocd-cm)
```yaml
data:
  kustomize.buildOptions: --load-restrictor LoadRestrictionsNone --enable-helm
```
- `--load-restrictor LoadRestrictionsNone`: kustomize's flag (values `LoadRestrictionsRootOnly`,
  the default, or `LoadRestrictionsNone`) that lets a kustomization load files from outside its
  root, for example a shared `../../common/config.json` in a configMapGenerator.
- `--enable-helm`: needed for `helmCharts:` in kustomizations; it is not an Argo CD Kustomize option
  by itself, so it goes into `kustomize.buildOptions`.
- `kustomize.buildOptions` applies to all Kustomize apps.

## 2. Multiple kustomize versions
Install binaries into the repo-server (init container + shared volume), then register:
```yaml
# argocd-cm
data:
  kustomize.path.<version>: /custom-tools/kustomize_<version>
  kustomize.buildOptions.<version>: --load-restrictor LoadRestrictionsNone   # per-version options
```
```yaml
# Application
spec:
  source:
    kustomize:
      version: <version>          # or: argocd app set <app> --kustomize-version <version>
```
Repo-server patch (the pattern from the Argo CD custom-tools docs: emptyDir volume, init container copies the binary, volume mounted into the repo-server):
```yaml
initContainers:
  - name: kustomize-v4
    image: <image-with-a-shell-and-download-tool>
    command: [sh, -c]
    args: ["<download the pinned kustomize release and place it at /custom-tools/kustomize_<version>>"]
    volumeMounts: [{ name: custom-tools, mountPath: /custom-tools }]
```
Mount the same `custom-tools` volume in the `argocd-repo-server` container.

## 3. Why versions matter
Rendering can differ between kustomize versions, so pin the version the team uses locally
(`kustomize version`) and register the same one in Argo CD, and use it in CI checks.

## Gotchas
- The built-in kustomize version follows the Argo CD release — upgrading Argo CD can change rendering. Diff `argocd app manifests` before and after upgrades.
- Remote bases are fetched at render time, so they need network access from the repo-server; consider vendoring them.

## Verify
- [ ] `argocd app manifests` renders without load-restrictor errors; `argocd version` / repo-server logs show the expected kustomize path.

## Checked

2026-10-25, against the Argo CD user guide (Kustomize), operator manual (argocd-cm reference, custom tools) and kustomize `flagloadrestrictor.go`. Confirmed: `kustomize.buildOptions`, `kustomize.path.<version>` and `kustomize.buildOptions.<version>` keys, `spec.source.kustomize.version` and `argocd app set --kustomize-version`, the init container + emptyDir pattern, kustomize's `--load-restrictor` flag and its two values, `--enable-helm` not being an Argo CD option. Removed as unconfirmed: the specific error message, pinned binary version and download URL, the kustomize v4 to v5 deprecation list, and the kubeconform pipeline.

Method: documentation only; no commands were run.

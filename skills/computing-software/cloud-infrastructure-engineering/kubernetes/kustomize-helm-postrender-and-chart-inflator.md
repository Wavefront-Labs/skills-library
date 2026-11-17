---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kustomize-helm-postrender-and-chart-inflator
name: kustomize-helm-postrender-and-chart-inflator
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kustomize, helm, helmcharts, postrenderer, argo-cd, argocd, chart-inflator, kustomize-build-options, enable-helm, helm-template, gitops, patching-rendered-output]
level: practitioner
status: verified
description: "Combine Helm and Kustomize safely: the helmCharts inflator, Argo CD's Kustomize postRenderer, and why patching rendered Helm output is risky."
sources: ["https://github.com/kubernetes-sigs/kustomize/blob/master/examples/chart.md", "https://github.com/kubernetes-sigs/kustomize/blob/master/api/types/helmchartargs.go", "https://argo-cd.readthedocs.io/en/stable/user-guide/kustomize/", "https://argo-cd.readthedocs.io/en/stable/user-guide/multiple_sources/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kustomize + Helm — three ways to combine them, and which one to actually use

**Problem this solves:** a third-party chart (ingress-nginx, cert-manager, a vendor
chart) doesn't expose a `values.yaml` knob you need, but you don't want to fork it.
Kustomize patches the *rendered* manifests after Helm templates them. There are three
distinct integration points with different blast radii — pick deliberately.

## 1. `kustomization.yaml` `helmCharts:` (the built-in inflator)
```yaml
helmCharts:
  - name: ingress-nginx
    repo: https://kubernetes.github.io/ingress-nginx
    version: 4.11.3
    releaseName: ingress-nginx
    namespace: ingress-nginx
    valuesFile: values-prod.yaml    # used INSTEAD of the chart's values.yaml; valuesInline / additionalValuesFiles also exist
    skipHooks: true                 # see below
    skipTests: true
patches:
  - target: {kind: Deployment, name: ingress-nginx-controller}
    patch: |-
      - op: add
        path: /spec/template/spec/containers/0/args/-
        value: --enable-ssl-passthrough
```
Field names (`repo`, `valuesFile`, `valuesInline`, `additionalValuesFiles`, `skipHooks`, `skipTests`, `includeCRDs`,
`kubeVersion`) come from `api/types/helmchartargs.go`; ingress-nginx 4.11.3 exists in the chart repo index.
- Requires `kustomize build --enable-helm`; without it the build stops with `must specify --enable-helm` (run on
  5.8.3). Argo CD does not pass the flag by default: its docs say to set `kustomize.buildOptions: --enable-helm` in
  the `argocd-cm` ConfigMap (global to all Kustomize apps) or use a config management plugin.
- It runs `helm template` under the hood, so Helm **hooks never fire**. Run on 5.8.3 with a local chart: a
  `pre-install` hook Job and the `helm.sh/test` Pod both rendered as ordinary resources, still carrying their
  `helm.sh/hook` annotations. `skipHooks: true` and `skipTests: true` removed them. Wrong for anything that relies
  on a hook-based migration.
- Charts are pulled with `helm pull --untar` into `charts/` next to the kustomization (`helmGlobals.chartHome`
  changes it) and an existing chart directory is reused, not re-fetched (Kustomize `examples/chart.md`). A chart
  outside the kustomization root needs `--load-restrictor=none`.

## 2. Argo CD
Argo CD has no Helm post-renderer in the `Application` spec. Choices: (a) `helmCharts:` in a Kustomize source with
`--enable-helm` set in `argocd-cm` as above; (b) a multi-source `Application` (`spec.sources:` with `ref:` and
`$values/...` value files; see Argo CD `multiple_sources.md`) which lets a Helm chart read value files from another repo. Hook mapping and ordering: see
`computing-software.devops-ci-cd.argo-cd.sync-waves-and-resource-hooks`.

## 3. Pipe `helm template` into a throwaway kustomization
Outside Argo CD: `helm template rel ./chart -f values.yaml > rendered.yaml`, then a `kustomization.yaml` with
`resources: [rendered.yaml]` and your patches, then `kustomize build .` (run: replicas patched from 1 to 7).
`kustomize build -` does not read stdin; it needs a directory (`must build at directory`), so the file is required.
Plain `helm template` keeps hook Jobs and test Pods in the output; add `--no-hooks --skip-tests` (run: both removed them). Nothing validates
that a chart upgrade keeps the resource names your patch `target:` selectors use.

## Decision guide
- Add one arg, label or sidecar to a vendored chart with no values knob: `helmCharts:` inflator (option 1).
- Argo CD managed: option 1 with the `argocd-cm` flag, or a plugin.
- Plain CI apply: option 3, followed by `kubeconform -strict` and, with a cluster, `kubectl diff`.
- Patching more than about three fields on a vendor chart: ask whether `values.yaml` overrides (`extraArgs`,
  `extraEnv`, `podAnnotations`) or a fork is simpler than brittle JSON6902 targets.

## Gotchas
- **An unmatched patch `target:` is a silent no-op.** Run on 5.8.3: a JSON6902 patch targeting a Deployment name that
  does not exist built successfully and changed nothing; correcting the name changed replicas from 3 to 9. A chart
  bump that renames a resource therefore silently drops your patch.
- `helmCharts:` needs network access to the chart repo on the first build.
- CRDs installed by a chart are not lifecycle-managed by this pipeline (see `helm-crd-lifecycle-and-deletion-risk`);
  `includeCRDs` controls whether they are rendered.

## Verify
- [ ] `kustomize build --enable-helm overlays/<env>` and your actual deploy path
      (Argo CD / CI) use the **same** flag — don't let local builds succeed while CI
      silently skips the Helm inflation step.
- [ ] After a chart version bump, diff the built output before and after, because an unmatched `target:` does not
      fail the build.
- [ ] Any resource depending on a Helm hook for correctness is NOT routed through the
      `helmCharts:` inflator, or you've confirmed the hook's absence doesn't matter.

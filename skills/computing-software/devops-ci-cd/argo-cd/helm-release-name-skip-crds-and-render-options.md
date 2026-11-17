---
id: computing-software.devops-ci-cd.argo-cd.helm-release-name-skip-crds-and-render-options
name: helm-release-name-skip-crds-and-render-options
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, helm-release-name, skip-crds, helm-kube-version, helm-template-rendering]
level: practitioner
status: docs-checked
description: "Control how Argo CD renders Helm charts: releaseName, skipCrds, kubeVersion/apiVersions, skipTests, and the consequences of helm template rendering (no release, no lookup)."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/helm/", "https://github.com/argoproj/argo-cd/blob/master/docs/operator-manual/application.yaml", "https://argo-cd.readthedocs.io/en/stable/user-guide/sync-options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Helm release name, skipCrds and rendering options

```yaml
spec:
  source:
    chart: kube-prometheus-stack
    repoURL: https://prometheus-community.github.io/helm-charts
    targetRevision: <chart-version>
    helm:
      releaseName: kps              # default: the Application name
      skipCrds: true                # do not render the chart's crds/ directory
      kubeVersion: "1.31.0"         # semver, no leading v; default: the destination cluster's version
      apiVersions: [monitoring.coreos.com/v1/ServiceMonitor]   # format [group/]version/kind; default: the cluster's API versions
      skipTests: true               # skip Helm test manifests
      passCredentials: false
```

## How Argo CD uses Helm
Argo CD runs `helm template` and applies the output itself. Consequences:
- Argo CD cannot tell install from upgrade: every operation is a sync, so `pre-install` and `pre-upgrade` hooks run together.
- Helm hooks are mapped to Argo CD hooks (`pre-install` and `pre-upgrade` → PreSync, `post-install` and `post-upgrade` → PostSync, `pre-delete` → PreDelete, `post-delete` → PostDelete); `helm.sh/hook-weight` → `argocd.argoproj.io/sync-wave`. Hooks `test-success`, `test-failure`, `pre-rollback` and `post-rollback` are not supported, and defining any Argo CD hook makes Argo CD ignore all Helm hooks.
- Random data such as `randAlphaNum` is regenerated on every comparison, so the app is permanently OutOfSync; set the value explicitly in values.

## releaseName
The default release name is the Application name. Changing it renames resources that template `.Release.Name`. Overriding it can also break charts that use the `app.kubernetes.io/instance` label, because Argo CD injects that label with the Application name for tracking. When migrating from `helm install`, set `releaseName` to the existing release name so resource names match.

## CRDs
Charts with CRDs in `crds/`: a resource too big for the 262144-byte annotation size limit needs the `ServerSideApply=true` sync option. Alternatively set `skipCrds: true` (CLI `--helm-skip-crds`) and manage CRDs in a separate app with an earlier sync wave.

## Verify
- [ ] Rendered names use the intended release name; no perpetual diff from generated values.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: `helm` fields in the reference application.yaml (`releaseName`, `skipCrds`, `kubeVersion` semver, `apiVersions` in `[group/]version/kind` form, `skipTests`, `passCredentials`), release-name caveat, Helm hook mapping table and warnings, `randAlphaNum` behaviour, 262144-byte annotation limit and ServerSideApply. The `apiVersions` example in the old skill lacked the kind. Removed unconfirmed claims (no release secret, `lookup`).

Method: documentation only; no commands were run.

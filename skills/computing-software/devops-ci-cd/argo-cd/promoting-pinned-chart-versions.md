---
id: computing-software.devops-ci-cd.argo-cd.promoting-pinned-chart-versions
name: promoting-pinned-chart-versions
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, chart-version-promotion, helm-chart-pinning, semver-range-targetrevision, applicationset-chart-version]
level: practitioner
status: docs-checked
description: "Promote Helm chart versions environment by environment with Argo CD: exact pins per env, semver ranges only in dev, version files read by ApplicationSets, and verification."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/helm/", "https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Git/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Promoting pinned chart versions

## 1. Per-environment version files
```text
platform/ingress-nginx/
  envs/dev/config.json      {"chartVersion": "4.11.4", "valuesFile": "values-dev.yaml"}
  envs/staging/config.json  {"chartVersion": "4.11.3", ...}
  envs/prod/config.json     {"chartVersion": "4.11.2", ...}
```
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata: { name: ingress-nginx, namespace: argocd }
spec:
  goTemplate: true
  generators:
    - git:
        repoURL: https://github.com/acme/platform-config.git
        revision: main
        files: [{ path: platform/ingress-nginx/envs/*/config.json }]
  template:
    metadata: { name: 'ingress-nginx-{{index .path.segments 3}}' }
    spec:
      project: platform
      sources:
        - repoURL: https://kubernetes.github.io/ingress-nginx
          chart: ingress-nginx
          targetRevision: '{{.chartVersion}}'
          helm: { valueFiles: ['$cfg/platform/ingress-nginx/{{.valuesFile}}'] }
        - { repoURL: https://github.com/acme/platform-config.git, targetRevision: main, ref: cfg }
      destination: { name: '{{index .path.segments 3}}', namespace: ingress-nginx }
```
Promotion = PR changing `chartVersion` in the next env's file.

## 2. Pinning policy
- Use exact chart versions in staging and prod, promoted after a soak period; a version constraint in prod would let an upstream publish change what prod renders without a commit.
- The Argo CD best-practices page recommends manifests at a Git revision be truly immutable (pin remote bases and chart versions instead of floating references).

## 3. Before promoting
Render the old and new chart versions with your values (`helm template ... --version <X>`), diff the output, and read the chart changelog for CRD changes.

## Verify
- [ ] Each env's Application shows the expected chart version as its target revision.

## Checked
2026-10-28. Confirmed on the ApplicationSet Git generator page: file (config.json) generator parameters, `goTemplate`, `{{index .path.segments n}}`, `{{.path.basename}}`; and on the multiple sources page the `$values`-style `ref` reference. Confirmed on the best-practices page: keep manifests at a Git revision immutable by pinning floating references.
Removed (not confirmed): the claim that Argo CD resolves chart version ranges on refresh, the dev range example, the Renovate suggestion and the `argocd app get` Revision wording.

Method: documentation only; no commands were run.

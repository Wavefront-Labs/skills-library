---
id: computing-software.devops-ci-cd.kustomize.gitops-layout-practices
name: gitops-layout-practices
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [gitops, layout, environments, base, overlays]
level: practitioner
status: docs-checked
description: "Lay out bases and overlays in git so changes produce a review, build and deploy cycle, using the glossary conventions."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/glossary/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The glossary ties kustomize to GitOps: a base configuration could be the sole content of a git repository dedicated to that purpose, and the same goes for overlays. Changes in a repo could generate a build, test and deploy cycle. It defines gitops as devops or CICD workflows that use a git repository as a single source of truth and take action (build, test or deploy) when that truth changes.

Common layout from the glossary:

```
base/
  deployment.yaml
  kustomization.yaml
  service.yaml
overlays/
  dev/
    kustomization.yaml
    patch.yaml
  prod/
    kustomization.yaml
    patch.yaml
  staging/
    kustomization.yaml
    patch.yaml
```

The three roots dev, prod and staging (presumably) all refer to the base root; one has to inspect their kustomization.yaml files to be sure.

Principles from the glossary on declarative application management: work with any configuration (bespoke, off-the-shelf, stateless, stateful), support common customizations and variants such as development, staging and production, expose and teach native Kubernetes APIs rather than hide them, add no friction to version control integration (reviews and audit trails), compose with other tools in a unix sense, and avoid crossing into templating or domain specific languages.

Bespoke versus off-the-shelf: a bespoke configuration is a kustomization and resources created and maintained internally by an organization; its workflow is simpler because there is no notion of periodically capturing someone else's upgrades.

A base has no knowledge of the overlays that refer to it. An overlay is unusable without its bases and may itself act as a base. Variants are built with, for example, `kustomize build someapp/overlays/staging | kubectl apply -f -`.

## Checked

2026-11-08: read the kustomize glossary page in full; confirmed the gitops, base, overlay, bespoke, declarative application management and kustomization root entries and the layout. Removed the three numbered practices (no environment names in a base, what to put in overlays, reviewing build diffs in pull requests), which are opinion and not stated by the glossary.

Method: documentation only; no commands were run.

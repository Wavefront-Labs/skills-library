---
id: computing-software.devops-ci-cd.argo-cd.kargo-warehouses-stages-and-freight
name: kargo-warehouses-stages-and-freight
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, kargo-stages, kargo-warehouse, kargo-freight, kargo-promotion-steps]
level: advanced
status: docs-checked
description: "Automate GitOps promotion with Kargo: Warehouses that discover artifacts, Freight, Stages with promotion steps that update Git and Argo CD, verification and auto-promotion."
sources: ["https://docs.kargo.io/user-guide/core-concepts/", "https://docs.kargo.io/user-guide/reference-docs/promotion-steps/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kargo: warehouses, stages and freight

## Concepts
- **Warehouse**: monitors one or more repositories for new revisions of artifacts and packages the latest revision of each into new Freight.
- **Freight**: a "meta-artifact" referencing specific revisions of artifacts such as container images and manifests.
- **Stage**: a promotion target; stages can be linked into a promotion pipeline.
- **Promotion**: propagating changes to a stage's desired state. It differs from deployment, which is left to a GitOps agent such as Argo CD.
- **Project**: unit of tenancy, associated with a Kubernetes namespace, so access is managed with Kubernetes RBAC.

## Promotion steps
Promotion templates are built from steps. The promotion steps reference documents, among others, `git-clone`, `kustomize-set-image`, `git-commit`, `git-push`, `git-open-pr`, `git-wait-for-pr` and `argocd-update`. A typical Git-based flow clones the config repo, sets the image, commits, pushes (or opens a PR and waits for it) and then updates the Argo CD Application. Step names and config fields change between Kargo versions: take exact YAML from the reference for your release.

## Verify
- [ ] A new image revision produces Freight in the Warehouse, and a promotion updates Git and the Argo CD Application.

## Checked
2026-10-28. Confirmed on the Kargo core concepts page: Promotions (distinct from deployments), Stages (promotion targets that can be linked into a pipeline), Freight (meta-artifact), Warehouses, Projects (backed by a namespace). Confirmed on the promotion steps reference: `git-clone`, `kustomize-set-image`, `git-commit`, `git-push`, `git-open-pr`, `git-wait-for-pr`, `argocd-update`.
Removed (not confirmed): the Warehouse and Stage YAML (`imageSelectionStrategy`, `requestedFreight`, `promotionTemplate`, `verification`), the verified-freight rule, the `kargo promote` command, auto-promotion policy text, and the `kargo.akuity.io/authorized-stage` annotation and credentials gotchas.

Method: documentation only; no commands were run.

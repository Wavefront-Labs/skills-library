---
id: computing-software.devops-ci-cd.argocd-image-updater.update-process-and-sync-policy
name: update-process-and-sync-policy
category: computing-software
field: devops-ci-cd
product: argocd-image-updater
tags: [argocd-image-updater, update-process, reconciliation-loop, sync-policy, auto-sync, rollback, strict-image-match]
level: intro
status: docs-checked
description: "The update flow: reconcile CRs, match applications, strict image-name check, registry lookup, write-back, and sync policy and rollback caveats."
sources: ["https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/basics/update.md", "https://github.com/argoproj-labs/argocd-image-updater/blob/master/docs/index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The update process, sync policy and rollback

Argo CD Image Updater is a controller that reconciles `ImageUpdater` CRs. For each CR:

1. list Argo CD `Application` resources in the CR's namespace and match them against `applicationRefs` (name patterns and label selectors)
2. process each match using the CR's image configurations (name, strategy, allowed tags, ignored tags, platforms)
3. check whether the image is actually deployed with the app; the check is strict on the full name including registry, so `docker.io/some/image` and `quay.io/some/image` are different (relax it with `forceUpdate`)
4. ask the registry for a newer version per the update strategy and constraints
5. if one exists, write it back per the update method

It never updates your manifests. It re-configures the Application sources to use the new tag and hands control to Argo CD.

Sync policy: if the Application has automatic sync, Argo CD deploys the new image; otherwise it is marked Out Of Sync and you sync manually. The updater works best with automatic syncing. Sync Windows and RBAC on Applications are fully supported.

Rollback: the updater does not honour an Application's rollback status and keeps updating to new images, although Argo CD disables auto-sync for rolled-back apps. Honouring rollbacks is on the roadmap.

Hard limitations: only Argo CD-managed apps; only Helm, Kustomize or Plugin (CMP) sources; for Helm the templates must accept the image tag (and maybe name) as a parameter such as `image.tag`.

## Checked

2026-11-08. Read in full: docs/basics/update.md, docs/index.md and docs/configuration/images.md (for forceUpdate). Confirmed the update steps, the strict image-name check and forceUpdate, the sync policy and rollback statements, and the Helm, Kustomize and Plugin limitation. Nothing removed.

Method: documentation only; no commands were run.

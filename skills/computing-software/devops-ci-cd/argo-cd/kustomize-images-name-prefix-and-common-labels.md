---
id: computing-software.devops-ci-cd.argo-cd.kustomize-images-name-prefix-and-common-labels
name: kustomize-images-name-prefix-and-common-labels
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, kustomize-images, name-prefix, common-labels, kustomize-replicas, kustomize-patches-in-app]
level: practitioner
status: docs-checked
description: "Set Kustomize overrides directly in Argo CD Applications: images, namePrefix/nameSuffix, commonLabels/annotations, namespace, replicas and patches, and when to keep them in Git."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/kustomize/", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_set/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kustomize images, namePrefix and commonLabels in the Application

```yaml
spec:
  source:
    repoURL: https://github.com/acme/deploy.git
    path: apps/api/base
    targetRevision: main
    kustomize:
      images:
        - acme/api:1.8.2                          # set tag
        - acme/worker=registry.acme.io/worker:1.8.2   # rename + tag
      namePrefix: pr-142-
      nameSuffix: ""
      namespace: preview-142
      commonLabels: { env: preview, pr: "142" }
      commonAnnotations: { owner: team-api }
      commonAnnotationsEnvsubst: true            # allow ${ARGOCD_APP_NAME} etc.
      replicas:
        - { name: api, count: 1 }
      patches:
        - target: { kind: Deployment, name: api }
          patch: |-
            - op: replace
              path: /spec/template/spec/containers/0/resources/requests/cpu
              value: 100m
```

## When to use the Application fields
- ApplicationSet-generated previews (per PR prefix/namespace/tag) — the Argo CD docs show inline `kustomize.patches` templated in an ApplicationSet; the same applies to the other fields.
Otherwise prefer a real overlay directory in Git (`overlays/prod/kustomization.yaml`) — reviewable and reproducible with plain `kustomize build`.

## CLI
```bash
argocd app set api-preview --kustomize-image acme/api:1.8.3
argocd app set api-preview --nameprefix pr-143-
argocd app set api-preview --kustomize-replica api=1
```
Same drift caveat as Helm parameters if the Application itself is managed from Git.

## Gotchas
- `commonLabels` also changes selectors by default → existing Deployments cannot be updated (immutable selector). Set `labelWithoutSelector: true` (and `labelIncludeTemplates` if the labels must reach pod templates), or avoid changing `commonLabels` after creation.
- `namePrefix` changes resource names → old resources pruned, new created (downtime for Services/PVCs).

## Verify
- [ ] `argocd app manifests` shows prefixed names, the image tag, and labels as intended.

## Checked

2026-10-25, against the Argo CD Kustomize user guide and the `argocd app set` command reference. Confirmed: the Application `spec.source.kustomize` fields (`namePrefix`, `nameSuffix`, `images`, `replicas`, `commonLabels`, `commonAnnotations`, `commonAnnotationsEnvsubst`, `namespace`, `patches`, `labelWithoutSelector`, `labelIncludeTemplates`), the CLI flags `--kustomize-image`, `--nameprefix`, `--kustomize-replica`, and the ApplicationSet use of inline patches. Replaced the `includeSelectors: false` advice with Argo CD's `labelWithoutSelector`; removed the unconfirmed Image Updater write-back remark. The `images` entry forms (`name:tag`, `name=new:tag`) follow the `--kustomize-image` help text.

Method: documentation only; no commands were run.

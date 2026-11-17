---
id: computing-software.devops-ci-cd.kustomize.patch-inline-strategic-merge
name: patch-inline-strategic-merge
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [patches, strategic-merge, inline, deployment]
level: practitioner
status: docs-checked
description: "Write strategic merge patches inline in kustomization.yaml, with or without a target, to set labels and container images."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/patches/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

An inline strategic merge patch is a string under `patch:` containing a partial resource. The docs use this `deployment.yaml` throughout (name `dummy-app`, label `app.kubernetes.io/name: nginx`, container `nginx` with image `nginx:stable`).

```yaml
resources:
- deployment.yaml
patches:
  - patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: dummy-app
        labels:
          app.kubernetes.io/version: 1.21.0
  - patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: not-used
      spec:
        template:
          spec:
            containers:
              - name: nginx
                image: nginx:1.21.0
    target:
      labelSelector: "app.kubernetes.io/name=nginx"
```

How it behaves:

- A patch may be a strategic merge patch or a JSON6902 patch, a file or an inline string, and may target one or several resources. Patches apply in the order listed.
- If a target is specified, the name in the patch metadata is required but not used.
- The target selects resources by group, version, kind, name, namespace, labelSelector and annotationSelector. The name and namespace selectors are automatically anchored regular expressions, so `myapp` means `^myapp$`.
- For a path-based strategic merge patch the page says the target can be omitted, in which case the resource is matched using the apiVersion, kind and name from the patch; the page says the inline form behaves the same.

The page states that all four strategies (inline and path-based strategic merge, inline and path-based JSON6902) lead to exactly the same build output for its two intents (pin the image, add a version label).

## Checked

2026-11-08: read the kustomize patches reference page in full; confirmed the example, target behaviour, anchored regex rule and the identical-output statement. Removed the claims that containers merge by name and the advice on when to choose strategic merge over JSON6902, which the page does not state.

Method: documentation only; no commands were run.

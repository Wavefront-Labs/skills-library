---
id: computing-software.devops-ci-cd.kustomize.kustomize-create
name: kustomize-create
category: computing-software
field: devops-ci-cd
product: kustomize
tags: [kustomize, create, init, scaffolding]
level: intro
status: docs-checked
description: "Bootstrap a kustomization.yaml in the current directory with kustomize create and optional flags for namespace, resources and labels."
sources:
  - https://kubectl.docs.kubernetes.io/references/kustomize/cmd/create/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`kustomize create` creates a new kustomization in the current directory. Run with no flags it makes an empty kustomization.yaml that you update by hand or with `kustomize edit` subcommands.

Example from the docs:

```bash
kustomize create --namespace=myapp --resources=deployment.yaml,service.yaml --labels=app:myapp
```

Output:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- deployment.yaml
- service.yaml
namespace: myapp
labels:
  app: myapp
```

Notes:

- `--resources` takes a comma-separated list.
- The command writes into the current directory, so `cd` to the target folder first.

## Checked

2026-11-08: confirmed against the kustomize create reference page, read in full (description, example command). Corrected the example output, which on the page shows `labels:` as a plain map (`app: myapp`), not a `pairs:` list. Removed the list of other command groups and the follow-up flow, which that page does not state.

Method: documentation only; no commands were run.

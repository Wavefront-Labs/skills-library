---
id: computing-software.devops-ci-cd.argo-cd.helm-parameters-and-file-parameters
name: helm-parameters-and-file-parameters
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, helm-parameters, file-parameters, force-string, argocd-app-set-helm]
level: practitioner
status: docs-checked
description: "Override individual Helm values in Argo CD with parameters and fileParameters, forceString, and why argocd app set overrides drift from Git in GitOps setups."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/helm/", "https://github.com/argoproj/argo-cd/blob/master/docs/operator-manual/application.yaml", "https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_app_set/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Helm parameters and file parameters

```yaml
spec:
  source:
    helm:
      parameters:
        - name: image.tag
          value: "1.8.2"
        - name: service.annotations.external-dns\.alpha\.kubernetes\.io/hostname   # escape dots in keys
          value: api.example.com
        - name: featureFlags.newCheckout
          value: "true"
          forceString: true          # keep as string "true", not boolean
      fileParameters:
        - name: config.json
          path: files/config.json    # file content becomes the value (relative to source path)
```
Equivalent to Helm `--set` / `--set-string` / `--set-file`. Order of precedence: `parameters > valuesObject > values > valueFiles > chart values.yaml`.

## CLI overrides
```bash
argocd app set api-prod -p image.tag=1.8.3
argocd app set api-prod --helm-set-string build=00123 --helm-set-file config.json=files/config.json
argocd app unset api-prod -p image.tag
argocd app get api-prod --show-params
```
These write into the **Application object**, so the override lives in the cluster and not in Git. In GitOps, change the Application YAML in Git instead.

## Gotchas
- Dots in a parameter name split keys; escape literal dots with a backslash (as in the annotation example above).
- Use `forceString: true` when a value such as `"true"` must stay a string.

## Verify
- [ ] `argocd app get <app> --show-params` lists the parameter; the rendered manifest has the exact string.

## Checked

Argo CD documentation, master branch (latest release v3.5.6), repository argoproj/argo-cd, last commit 2026-10-24. Checked 2026-10-25. Confirmed: `parameters` (with `forceString`) and `fileParameters` fields and the `\.` escape against the reference application.yaml, value precedence order, CLI flags `-p/--parameter`, `--helm-set-string`, `--helm-set-file`, `app unset -p`, `app get --show-params`. Removed unconfirmed parsing and Image Updater remarks.

Method: documentation only; no commands were run.

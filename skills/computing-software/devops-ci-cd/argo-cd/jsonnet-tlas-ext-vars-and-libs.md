---
id: computing-software.devops-ci-cd.argo-cd.jsonnet-tlas-ext-vars-and-libs
name: jsonnet-tlas-ext-vars-and-libs
category: computing-software
field: devops-ci-cd
product: argo-cd
tags: [argo-cd, jsonnet-tla, jsonnet-ext-vars, jsonnet-libs, jsonnet-applications]
level: advanced
status: docs-checked
description: "Render Jsonnet in Argo CD directory apps with top-level arguments, external variables and a shared library path."
sources: ["https://argo-cd.readthedocs.io/en/stable/user-guide/jsonnet/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Jsonnet: TLAs, ext vars and libs

Argo CD renders `*.jsonnet` files in a directory source. Jsonnet apps can use the standard build environment (for example `$ARGOCD_APP_NAME`) in TLAs and external variables, and a shared library such as a `vendor` folder relative to the repository root.
```yaml
spec:
  source:
    directory:
      jsonnet:
        extVars:
          - name: app
            value: $ARGOCD_APP_NAME
        tlas:
          - name: name
            value: $ARGOCD_APP_NAME
```
CLI equivalent for the library path: `--jsonnet-libs 'vendor'`. The Jsonnet page of the user guide has the full field list.

## Verify
- [ ] The manifests Argo CD renders match your local jsonnet output.

## Checked
2026-10-28. Confirmed on the Argo CD Jsonnet user guide and build environment text: TLAs and external variables can use build environment variables such as `$ARGOCD_APP_NAME`; the declarative `directory.jsonnet.extVars` / `tlas` name-value form; shared library paths relative to the repo root; the `--jsonnet-libs` CLI flag.
Removed (not confirmed): the `code: true` option, explicit `libs` field and example list, the jb install note, output-shape and `include` rules, and the local `jsonnet` command line.

Method: documentation only; no commands were run.

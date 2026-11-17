---
id: computing-software.data-engineering.kestra.github-actions-cicd
name: github-actions-cicd
category: computing-software
field: data-engineering
product: kestra
tags: [github-actions, cicd, validate-flows, deploy-flows, namespace-files, readonly]
level: practitioner
status: docs-checked
description: "Validate and deploy Kestra flows and namespace files from GitHub Actions with the official actions, their inputs, and an example workflow."
sources:
  - https://kestra.io/docs/version-control-cicd/cicd/github-action
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Official actions:

- `kestra-io/validate-flows-action-v2`
- `kestra-io/deploy-flows-action-v2`
- `kestra-io/deploy-namespace-files-action`

Inputs:

- Flows: `directory` (default `./`), `server` (required), `user`/`password`, `apiToken` and `tenant` (default `main`; Enterprise and Cloud only). Deploy adds `namespace` (else each flow keeps its own) and `override` (default `'false'`).
- Namespace files: `localPath` (default `./`), `namespacePath` (required), `namespace` (required), `override`.

```yaml
name: Kestra CI/CD
on: [push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: kestra-io/validate-flows-action-v2@main
        with:
          directory: ./kestra/flows
          server: ${{ secrets.KESTRA_HOSTNAME }}
  deploy:
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v4
      - uses: kestra-io/deploy-flows-action-v2@main
        with:
          directory: ./kestra/flows/product
          namespace: product
          server: ${{ secrets.KESTRA_HOSTNAME }}
```

Caveats:

- The instance must be reachable from the runner (public or self-hosted runner).
- For offline validation use the legacy `kestra-validate-action`.
- For CI/CD-managed flows, add the label `system.readOnly` set to `"true"` to disable UI editing, especially for critical production flows.
- Keep tokens and credentials in GitHub Secrets.

## Checked

2026-11-04. Confirmed against the Kestra GitHub Actions page: the three official actions, input tables with defaults (directory ./, tenant main, override 'false', localPath ./), required inputs, reachability from the runner, the legacy kestra-validate-action for offline validation, system.readOnly label, GitHub Secrets advice, example workflow. Nothing removed.

Method: documentation only; no commands were run.

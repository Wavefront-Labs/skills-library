---
id: computing-software.devops-ci-cd.helm.dry-run-modes
name: dry-run-modes
category: computing-software
field: devops-ci-cd
product: helm
tags: [dry-run, debug, client, server, hide-secret, lookup, validation]
level: practitioner
status: docs-checked
description: "Choose between client-side and server-side dry runs for install and upgrade, and how --debug and --hide-secret fit in."
sources:
  - https://helm.sh/docs/helm/helm_install/
  - https://helm.sh/docs/helm/helm_upgrade/
  - https://helm.sh/docs/helm/helm_template/
  - https://helm.sh/docs/chart_template_guide/debugging/
  - https://helm.sh/docs/helm/helm_uninstall/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`--dry-run` simulates the operation without persisting changes. In the Helm 4 reference, `helm install` and `helm upgrade` accept `none` (the default; executes normally), `client` or `server`. `helm template` takes `client` or `server` and defaults to `client`. In the Helm 3 pages the install flag is `--dry-run string[="client"]` with `client` and `server` only.

- `--dry-run=client` simulates client-side only and avoids cluster connections.
- `--dry-run=server` simulates and validates the operation on the server and requires cluster connectivity. The debugging guide adds that it also executes any `lookup` in the chart against the server.

The debugging guide lists the commands that help with templates:

- `helm lint` verifies that the chart follows best practices.
- `helm template --debug` tests rendering locally.
- `helm install --dry-run --debug` renders without installing and also checks whether conflicting resources are already running on the cluster.
- `helm get manifest` shows what templates are installed on the server.

```bash
helm install demo ./chart --dry-run=server --debug --hide-secret
```

`--hide-secret` hides Kubernetes Secrets in dry-run output, which matters when the log goes to CI. The install and upgrade references warn that dry-run output includes Secrets, which can contain sensitive values, and to consider carefully how and when the flag is used.

If YAML does not parse but you want to see the output, comment out the problem lines in the template (`# {{ .Values.foo | quote }}`) and rerun with `--dry-run --debug`; the rendered comment shows the generated content.

When a `lookup` comes back empty, run with `--debug`: Helm logs "lookup: resource not found" or "lookup: resource list not found". Common causes are a missing resource, RBAC denial, `helm template` without cluster access, or wrong apiVersion, kind, namespace or name.

`helm uninstall --dry-run` (a plain boolean flag) shows which releases would be uninstalled.

## Checked

2026-11-08. Checked against the Helm 4 install, upgrade and template pages: --dry-run none|client|server (install default none; helm template defaults to client). Removed unsourced claims.

Method: documentation only; no commands were run.

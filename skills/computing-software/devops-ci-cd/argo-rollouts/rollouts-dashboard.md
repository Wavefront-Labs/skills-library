---
id: computing-software.devops-ci-cd.argo-rollouts.rollouts-dashboard
name: rollouts-dashboard
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [dashboard, ui, kubectl-plugin, localhost, address, argo-rollouts]
level: intro
status: docs-checked
description: "Start the local Argo Rollouts UI dashboard with the kubectl plugin and view Rollouts on port 3100."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/dashboard/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The kubectl plugin can serve a local UI that shows a list of Rollouts and a detailed view of each one. Run it in the namespace that contains your Rollouts:

```bash
kubectl argo rollouts dashboard
```

Then browse to `localhost:3100`.

Flags from the command reference: `--port` (`-p`) sets the listening port (default 3100) and `--root-path` changes the dashboard's root path (default `rollouts`).

The UI has a list view and an individual Rollout view. For scripts use the CLI (`get rollout NAME -w`, `status`).

The dashboard is served locally by the kubectl plugin, not by the controller.

Verify: the page at `localhost:3100` lists your Rollouts. If it is empty, check you ran the command in the namespace that contains your Rollouts (`-n`) and with the right kubeconfig context.

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/dashboard/, https://argo-rollouts.readthedocs.io/en/stable/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_dashboard/.

Removed or corrected: the security note about v1.8.5/v1.9.2/v1.10.1, the 127.0.0.1 default and the --address flag (not on the pages), the Argo CD UI advice and the claim about what clicking a Rollout shows.

Method: documentation only; no commands were run.

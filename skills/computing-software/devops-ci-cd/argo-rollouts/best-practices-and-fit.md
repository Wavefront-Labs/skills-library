---
id: computing-software.devops-ci-cd.argo-rollouts.best-practices-and-fit
name: best-practices-and-fit
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [best-practices, applicability, progressive-delivery, metrics, downward-api, ingress-host-routes, argo-rollouts]
level: practitioner
status: docs-checked
description: "Judge whether an application and team are ready for Argo Rollouts and apply the project's own best practices."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/best-practices/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Guidance from the project documentation.

**Check application compatibility.** Apps writing to shared files have issues, and queue-consuming workers rarely work without extra support. Using Rollouts for infrastructure apps such as cert-manager, nginx, coredns or sealed-secrets is not recommended.

**Know the scope.** One Kubernetes application in a single cluster; the controller must run in every cluster that has Rollouts. It does not need Argo CD or any other Argo project.

**Fit.** Designed for brief deployments of 15-20 minutes, at most 1-2 hours. Not for preview or ephemeral environments (use the Argo CD Pull Request generator), nor for running versions side by side for days. If 1.5 is deployed while 1.4 is preview and 1.3 stable, it keeps 1.3 stable and previews 1.5, and rolls back to 1.3.

**Prepare metrics first.** The end goal is fully automated deployments and rollbacks; you should get a verdict from metrics in 5-15 minutes. Test them with dry-runs before production.

**No separate API.** Use the Kubernetes API, CLI or notifications to integrate.

**Downward API.** Use ephemeral labels so apps adapt during canaries.

**Ingress host routes.** Add extra host rules to the Ingress so tests can reach the preview/canary or stable pods directly.

Verify readiness: do you have metrics that tell you within 5-15 minutes whether a deployment is successful?

## Checked

2026-11-03. Confirmed against the Argo Rollouts documentation pages: https://argo-rollouts.readthedocs.io/en/stable/best-practices/.

Removed or corrected: the ten-minute verification wording (the page says 5-15 minutes).

Method: documentation only; no commands were run.

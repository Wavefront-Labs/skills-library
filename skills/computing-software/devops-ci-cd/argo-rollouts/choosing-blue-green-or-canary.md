---
id: computing-software.devops-ci-cd.argo-rollouts.choosing-blue-green-or-canary
name: choosing-blue-green-or-canary
category: computing-software
field: devops-ci-cd
product: argo-rollouts
tags: [blue-green, canary, strategy, progressive-delivery, traffic-manager, argo-rollouts]
level: practitioner
status: docs-checked
description: "Decide between blue-green, basic canary and traffic-managed canary using Argo Rollouts' own comparison table."
sources:
  - https://argo-rollouts.readthedocs.io/en/stable/concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Argo Rollouts supports only Blue-Green and Canary (RollingUpdate is the default strategy of the Deployment object, and Recreate means downtime). The docs recommend starting with blue-green and moving to canaries as you gain confidence in your metrics and applications.

Why blue-green first:

- It always works, because only one version serves traffic at a time. Not every application tolerates two versions running in parallel, which can block canaries for legacy apps.
- You get its full value without a traffic manager. Canaries work without one, but their advanced features assume fine-grained traffic control.
- It suits queue-consuming workers and shared or locked resources, since Argo Rollouts does not control traffic on connections it does not understand, such as binary or queue channels.

Summary from the concepts page:

| | Blue/Green | Basic canary | Canary + traffic manager |
|---|---|---|---|
| Adoption complexity | Low | Medium | High |
| Needs traffic provider | No | No | Yes |
| Works with queue workers | Yes | No | No |
| Traffic switch | All or nothing | Gradual % | Gradual % |
| Traffic control | 0% or 100% | Coarse (pod counts) | Fine grained |
| Failure blast radius | Massive | Low | Low |

The traffic manager can be a service mesh, an ingress controller, or a Gateway API implementation via plugin.

Self-check: ask whether two versions can safely coexist and whether you have a traffic router. No to the first means blue-green.

## Checked

2026-11-08. Confirmed against the Argo Rollouts concepts page (read in full): supported strategies, why blue-green first, the comparison table rows quoted, and traffic manager options.

Removed or corrected: replaced the claim that RollingUpdate and Recreate are Deployment behaviour with the page's descriptions.

Method: documentation only; no commands were run.

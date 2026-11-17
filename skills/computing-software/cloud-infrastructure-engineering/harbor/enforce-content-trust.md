---
id: computing-software.cloud-infrastructure-engineering.harbor.enforce-content-trust
name: enforce-content-trust
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [content-trust, cosign-policy, notation-policy, deployment-security, harbor]
level: practitioner
status: docs-checked
description: "Make a Harbor project allow only verified images to be pulled by enabling the Cosign or Notation deployment policy."
sources:
  - https://goharbor.io/docs/main/working-with-projects/project-configuration/implementing-content-trust/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Harbor supports artifact signing and verification through Cosign and Notation. A project administrator enforces it with the default deployment security policy for a project.

Steps:
1. Log in and open the project **Configuration** tab.
2. Tick **Cosign** or **Notation**. You can tick both to require both policies.
3. Click **Save**.

Effect: Harbor only allows verified images to be pulled from the project. Verification is determined by the policy you ticked: Cosign signatures or Notation signatures.

Consequences you will hit:
- Unsigned images cannot be pulled. The Helm OCI charts page repeats the warning for projects with content trust enforced.
- Signing is done outside Harbor with the `cosign` or `notation` CLI, which push the signature to Harbor; see the signing skills for those commands.
- Vulnerability scans of Cosign signatures are not supported.


The setting lives on each project Configuration tab, so every project is configured separately. When both options are ticked, both Cosign and Notation policies apply.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Implementing Content Trust, Sign Artifacts, Helm OCI charts.
- Removed: the claim that Helm charts specifically are blocked (the page says unsigned images).
Method: documentation only; no commands were run.

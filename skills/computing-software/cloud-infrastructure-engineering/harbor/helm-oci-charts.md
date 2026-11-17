---
id: computing-software.cloud-infrastructure-engineering.harbor.helm-oci-charts
name: helm-oci-charts
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [helm, oci-chart, helm-push, helm-registry-login, harbor]
level: intro
status: docs-checked
description: "Push, pull and install Helm charts stored as OCI artifacts in Harbor with helm registry login, helm push and helm pull."
sources:
  - https://goharbor.io/docs/main/working-with-projects/working-with-oci/working-with-helm-oci-charts/
  - https://goharbor.io/docs/main/administration/configure-project-quotas/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since Helm 3.8.0, charts can be stored in container registries as OCI artifacts, and Harbor supports this.

Log in first (required for private projects, and for pushing):
`helm registry login <harbor_address>`

Pull a chart:
`helm pull oci://<harbor_address>/<project>/<chart_name> --version <version>`
For example `helm pull oci://demo.goharbor.io/oci/demo --version 0.1.0`.

Push a chart: create the project in Harbor first (or use an existing one), log in, then
`helm push <chart_name_and_version>.tgz oci://<harbor_address>/<project>`
For example `helm push example-0.1.0.tgz oci://demo.goharbor.io/oci`. The push target is the project path, not a chart name.

Gotchas:
- You cannot push charts or images to a proxy cache project.
- If the project enforces content trust (Cosign or Notation), you cannot pull an unsigned chart.
- Helm chart size is not counted in project storage quotas.


Install a chart straight from the registry: `helm install <release_name> oci://<harbor_address>/<project>/<chart_name> --version <version>`, for example `helm install MyRelease oci://demo.goharbor.io/oci/demo --version 0.1.0`. If the project is private, run `helm registry login` first as above.

## Checked

2026-11-03. Helm 3.8.0 statement, login, pull, push and install commands, proxy cache push restriction and content trust restriction were read against the Harbor docs page Working with OCI Helm Charts. The quota statement (Helm chart size is not calculated) was read on the Configure Project Quotas page. Nothing removed.

Method: documentation only; no commands were run.

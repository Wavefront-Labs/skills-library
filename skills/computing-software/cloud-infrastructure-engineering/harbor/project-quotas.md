---
id: computing-software.cloud-infrastructure-engineering.harbor.project-quotas
name: project-quotas
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [project-quota, storage-quota, default-quota, quota-accounting, harbor]
level: practitioner
status: docs-checked
description: "Set global default and per-project storage quotas in Harbor and understand how pushes, retags, shared blobs and GC affect usage."
sources:
  - https://goharbor.io/docs/main/administration/configure-project-quotas/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default all projects have unlimited storage. A system administrator can set a global default and per-project quotas in the **Project Quotas** view.

- Global default: click **Edit**, enter **Default storage consumption** in `MiB`, `GiB` or `TiB`, or enter `-1` for unlimited.
- Individual project: select the project, click **Edit** and enter its limit. A per-project quota overrides the global default.
- The default applies only to projects created after you set or change it, not to existing projects.

How usage is calculated:
- Harbor computes image size when blobs and manifests are pushed. The manifest is pushed last, after its blobs succeed. With concurrent pushes and too little quota for all of them, images are accepted in the order their manifests arrive, so a push may not be rejected immediately.
- Shared blobs count once per project. Quota is tracked per project, so a blob referenced by several projects is counted in each, and total reported usage can exceed physical storage.
- Retagging inside a project does not change usage because there are no new blobs or manifests. Retagging from one project to another increases usage.
- Garbage collection frees storage used by untagged blobs in the project.
- Helm chart size is not counted.

After setting quotas, the view shows how much of its quota each project has consumed.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Configure Project Quotas.
Method: documentation only; no commands were run.

---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.container-and-serverless-assets
name: container-and-serverless-assets
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [container-and-serverless-assets, cloud-and-virtual-asset-management, kubernetes, containers, images, serverless, ephemeral, registry inventory, itam-licence-compliance]
level: advanced
status: draft
description: "Inventory ephemeral container images, clusters and functions, and tie them to owners and licensed software."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Containers, Kubernetes and serverless as assets

Goal: visibility into short-lived workloads without per-pod records.

Method:
- Treat clusters, namespaces, registries and base images as the assets; pods are runtime state.
- Label namespaces with owner and cost-centre; enforce via admission policy.
- Inventory images from registries and generate SBOMs per image (see SBOM skills).
- Licence metrics: commercial software in containers may count per host core or per container (vendor-specific; confirm).
- Capture serverless function runtimes and dependencies via build pipeline.

Gotchas:
- Node autoscaling changes licence core counts daily; use peak and averages as vendor rules require.
- Public base images carry copyleft obligations.

Verify: every running image maps to a registry entry with an owner label.

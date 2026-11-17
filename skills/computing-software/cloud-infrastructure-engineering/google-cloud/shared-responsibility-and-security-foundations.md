---
id: computing-software.cloud-infrastructure-engineering.google-cloud.shared-responsibility-and-security-foundations
name: shared-responsibility-and-security-foundations
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, shared-responsibility, shared-fate, security-foundations-blueprint, enterprise-foundations-blueprint, security-baseline, control-matrix, iaas-paas-saas-responsibility, compliance-mapping, cis-gcp-benchmark, security-architecture, defense-in-depth, responsibility-matrix, risk-protection-program, cyber-insurance]
level: practitioner
status: docs-checked
description: "Turn the GCP shared responsibility model into a per-service control matrix: IaaS/PaaS/SaaS split, shared fate, enterprise foundations blueprint, Cyber Insurance Hub."
sources: ["https://docs.cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate", "https://docs.cloud.google.com/architecture/blueprints/security-foundations", "https://cloud.google.com/security/products/risk-protection-program", "https://www.cisecurity.org/benchmark/google_cloud_computing_platform"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shared responsibility and security foundations

**Goal:** a one-page matrix that says, for every service you use, which controls Google operates and which you must, and a baseline that proves your side is done.

## 1. The model (as Google documents it)
| Service type | Examples in Google's doc | Split |
|---|---|---|
| IaaS | Compute Engine, Cloud Storage, Cloud VPN, Cloud Load Balancing, Cloud DNS | The bulk of security responsibilities are yours; Google's focus on the underlying infrastructure and physical security |
| PaaS | App Engine, GKE, BigQuery | Google is responsible for more controls than in IaaS, varying by service and feature; you share responsibility for application-level controls and IAM management and remain responsible for data security and client protection |
| SaaS | Google Workspace, Google Security Operations, Marketplace SaaS | Google owns the bulk; you remain responsible for access controls and the data you store |
| FaaS/serverless | Cloud Run functions | Similar list to SaaS |

Always true per the doc: the provider remains responsible for the underlying network and infrastructure, and customers always remain responsible for their access policies and data. Which controls you must implement also depends on your regulatory obligations, your security standards and risk plan, and customer and vendor requirements; responsibilities are also defined by industry framework (for example PCI DSS, HIPAA) and by location (for example GDPR data residency in EU regions).

Inherited controls (such as Google's default encryption and infrastructure controls) can be offered as evidence of your posture to auditors and regulators.

## 2. Shared fate
Google's term for what it does beyond shared responsibility:
- Help getting started: the enterprise foundations blueprint, secure blueprints (for example the secured data warehouse) deployed as IaC, Well-Architected Framework security guidance, and landing zone navigation guides (resource hierarchy, identity onboarding, security and key management, network structure).
- Risk Protection Program with Cyber Insurance Hub (section 5).
- Governance products named in the doc: Assured Workloads, Security Command Center Premium, organization policies and resource settings, Policy Intelligence tools, Confidential Computing, and Sovereign Controls by Partners (available in certain countries).

## 3. Build the matrix (per service, per control family)
Google's doc suggests listing your workloads by IaaS/PaaS/SaaS type and using its responsibility diagram as a checklist, listing your regulatory requirements, and verifying your side after deployment with Cyber Insurance Hub, Assured Workloads, Policy Intelligence and Security Command Center Premium.

Suggested columns: control family, Google responsibility, your responsibility, how you implement it (Terraform module, org policy, runbook), evidence. Include rows for the challenges the doc names: encryption key management location, incident management (needs close collaboration with the provider), and keeping up with threats. Keep the matrix in the repo next to the landing zone and review it when you adopt a service or regulations change.

## 4. Enterprise foundations blueprint
The enterprise foundations blueprint (formerly the security foundations blueprint) is a `terraform-example-foundation` GitHub repository of deployable Terraform plus a guide. Use it to build a foundation or to review an existing environment against Google's recommendations. Its defense-in-depth model combines three control types:
- Policy controls: programmatic constraints, using IaC validation in the pipeline and organization policy constraints.
- Architecture controls: configuration of resources such as networks and the resource hierarchy.
- Detective controls: Security Command Center, integration with a SOC, and custom detective controls.

Key decisions it records: Terraform in version control deployed by Cloud Build with policy-as-code checks; identities synced from your identity provider; allow policies applied to groups by job function; one organization with folders per environment and labelled projects; Shared VPC with all network paths private and no outbound or inbound public internet traffic by default; aggregated log sinks to a central project; organization policy constraints against high-risk configurations; centralised Secret Manager and Cloud KMS projects; Security Command Center for detection. Record deviations from these as risk acceptances in the matrix.

## 5. Risk Protection Program and Cyber Insurance Hub
Cyber Insurance Hub scans Google Cloud workloads, produces a report mapped against CIS Benchmarks, and can share it with partner insurers (Beazley, Chubb and Munich Re are named on the product page) from the UI. It only scans Google Cloud workloads. It is available at no additional charge; Security Command Center Standard is required for it to run, and an Organization Administrator or Security Administrator enables it. Google is not a licensed broker and does not issue policies: you work with a licensed broker, and pricing is set by the insurers. The product page marks the product as Preview.

## 6. CIS Benchmark
CIS publishes a Google Cloud Platform Foundation benchmark (version 5.0.0 listed on the CIS page at the review date) as a free PDF for non-commercial use. Check the current version on the CIS page before mapping controls.

## Gotchas
- Google being certified covers Google's side only; an auditor still wants your IAM, logging and change-management evidence.
- Misconfiguration is named by Google as the root cause of most security breaches; secure starting configurations reduce it.
- Third-party SaaS from Marketplace is a three-party situation (vendor, Google, you); record it.

## Verify
- [ ] The matrix exists in the repo and covers every service in use, and each "you" cell links to an implemented control.
- [ ] A sampled control has evidence an auditor could pull without engineering help.
- [ ] The matrix was updated at the last new-service adoption.

## Checked
2026-11-08: confirmed against Google's "Shared responsibilities and shared fate on Google Cloud" page, the Enterprise foundations blueprint page, the Risk Protection Program product page and the CIS Google Cloud benchmark page. Removed: the per-layer table of Titan/hypervisor/OS patching rows, the specific org policy and SCC finding names, the 9-point baseline list, CIS control-number mapping, VM Manager and GKE patching claims, and the "priced on your SCC posture" and "requires SCC Premium" claims (the page says Standard is required for the Hub), none of which the cited pages state. Dropped sources: the security whitepaper and compliance hub (not used for any remaining claim).
Method: documentation only; no commands were run.

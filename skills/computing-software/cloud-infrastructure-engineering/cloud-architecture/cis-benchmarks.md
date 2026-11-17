---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cis-benchmarks
name: cis-benchmarks
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-security-architecture, cis-benchmarks, security-baseline, cis-foundations-benchmark, hardened-images, cis-level-1, kube-bench, baseline-exceptions]
level: practitioner
status: draft
description: "Adopt CIS benchmarks as the security baseline for cloud accounts, OS images and Kubernetes: level 1 vs 2, automated assessment, hardened images, and managing documented exceptions."
sources: ["https://www.cisecurity.org/cis-benchmarks", "https://docs.aws.amazon.com/securityhub/latest/userguide/cis-aws-foundations-benchmark.html", "https://github.com/aquasecurity/kube-bench"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security baselines with CIS benchmarks

## Layers
| Layer | Benchmark | Assessment |
|---|---|---|
| Cloud account | CIS AWS / Azure / GCP Foundations | Security Hub CIS standard, Defender for Cloud regulatory compliance, SCC compliance, Prowler/ScoutSuite |
| OS images | CIS Linux/Windows benchmarks | CIS-CAT, OpenSCAP, Inspector CIS scans; CIS hardened images in marketplaces |
| Kubernetes | CIS Kubernetes, EKS/AKS/GKE benchmarks | kube-bench; managed services cover control-plane items |
| Databases/containers | CIS Docker, PostgreSQL, etc. | tool-specific |

## Steps
1. Adopt **Level 1** (practical, low-impact) everywhere; **Level 2** for high-security workloads after testing.
2. Bake OS hardening into the **golden image pipeline** (Packer + Ansible/CIS roles, EC2 Image
   Builder, Azure Image Builder) rather than hardening at runtime.
3. Automate account-level checks continuously via CSPM.
4. **Exceptions register**: control id, reason, compensating control, owner, expiry — reviewed quarterly.
5. Map benchmark version; update when CIS releases new versions (control ids change).

## Gotchas
- Blindly applying Level 2 OS controls can break applications (e.g. disabled kernel modules, strict mount options).
- Benchmarks lag new services — not a substitute for threat modelling.

## Verify
- [ ] Account-level CIS compliance ≥ target with exceptions documented.
- [ ] Golden images scanned in CI before publishing.

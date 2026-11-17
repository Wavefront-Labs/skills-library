---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.defense-in-depth
name: defense-in-depth
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, security-foundations, cloud-security-architecture, defense-in-depth, layered-security, control-layers, assume-breach]
level: practitioner
status: draft
description: "Layer cloud controls so one failure doesn't mean compromise: org guardrails, identity, network, workload, data and detection layers, with an assume-breach review."
sources: ["https://learn.microsoft.com/azure/well-architected/security/principles", "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/security.html", "https://csrc.nist.gov/pubs/sp/800/207/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Defence in depth layering

## Layers (outer to inner)
1. **Organisation guardrails**: SCPs / management group policies / org policies (deny disabling
   logging, restrict regions, block public sharing).
2. **Identity**: phishing-resistant MFA, conditional access, least privilege, JIT admin.
3. **Network**: edge WAF/DDoS, private endpoints, segmentation, egress filtering.
4. **Compute/workload**: hardened images, patching, runtime protection, no SSH keys (session manager).
5. **Application**: authn/authz, input validation, secrets from vaults.
6. **Data**: encryption with managed keys, data perimeter (VPC endpoint policies, resource policies
   restricted to org), backups immutable.
7. **Detection and response**: threat detection services, centralised logs, alerting, playbooks.

## Assume-breach review
For each layer ask: "If this layer fails (stolen credential, exposed port, vulnerable library),
what stops or detects the attacker at the next layer?" Example: a leaked developer key is limited
by least privilege, blocked by SCP from disabling CloudTrail, and detected by anomalous API alerts.

## Gotchas
- Relying solely on the network perimeter (flat network inside).
- Duplicated controls at one layer instead of distinct ones across layers.

## Verify
- [ ] Assume-breach walkthrough documented for the top 3 attack paths.

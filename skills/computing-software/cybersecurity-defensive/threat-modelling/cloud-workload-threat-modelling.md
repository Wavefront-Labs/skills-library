---
id: computing-software.cybersecurity-defensive.threat-modelling.cloud-workload-threat-modelling
name: cloud-workload-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling, cloud-threat-modelling, aws, azure, iam, control-plane, data-flow-diagram, stride]
level: advanced
status: draft
description: "Threat model cloud workloads: control plane vs data plane, IAM as the perimeter, metadata services, managed service trust boundaries and cloud-specific attack paths."
sources: ["https://cloudsecurityalliance.org/research/topics/threat-modeling", "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html", "https://attack.mitre.org/matrices/enterprise/cloud/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud workload threat modelling

**Goal:** apply threat modelling to cloud systems with the elements that matter there:
identities and policies, the provider control plane, managed services and account boundaries.

## Extend the DFD
Besides processes, stores and flows, draw:
- **Control plane** (cloud APIs: IAM, resource management) as an external process every
  admin, CI/CD pipeline and workload role can call. Most cloud breaches go through it.
- **Identities**: human roles/SSO, CI/CD deploy roles, workload roles/managed identities,
  cross-account roles, third-party access. Each is an entry point with a permission set.
- **Account/subscription/project boundaries** and VPC/VNet boundaries as trust boundaries.
- **Managed services** (S3, queues, databases, KMS) with their resource policies.
- **Metadata service** (IMDS) as a credential source on each compute node.

## Cloud-specific threats to walk through (ATT&CK Cloud matrix)
- Stolen long-lived access keys from code, CI variables, laptops; leaked via public repos.
- SSRF to the metadata service to steal workload credentials (mitigate: IMDSv2, hop limit).
- Over-privileged roles: `iam:PassRole` + compute create = privilege escalation; wildcard
  `s3:*` on all buckets.
- Resource policies granting public or cross-account access (S3, KMS key policies, SNS/SQS,
  Lambda permissions).
- CI/CD pipeline compromise using its deploy role (often admin).
- Disabling logging (CloudTrail stop, diagnostic settings delete) and guardrail tampering.
- Data exfiltration via snapshots shared to attacker accounts or public AMIs.
- Region and service sprawl: resources in unmonitored regions (crypto mining).
- Tenant isolation in multi-tenant SaaS built on shared cloud resources.

## Mitigation patterns
Least-privilege roles with permission boundaries, SCPs/Azure Policy guardrails (deny
disabling logging, deny public resources, restrict regions), short-lived credentials via
federation (no IAM users), IMDSv2, private endpoints, KMS with key policies separating
admins from users, separate accounts per environment, centralised logging in a locked
log archive account, detection (GuardDuty/Defender for Cloud).

## Output
Threat list keyed to identities and resources; for each, the guardrail/preventive control,
detection, and owner. Include an IAM attack-path analysis (PMapper, Cloudsplaining, or
CSPM attack path features) as evidence.

## Gotchas
- Treating the VPC as the perimeter while the control plane is open to any stolen key.
- Ignoring the deploy pipeline: it is usually the most privileged identity.

## Verify
Pick the top three threats and test controls: attempt to disable CloudTrail with a dev role
(denied by SCP), attempt IMDSv1 access (blocked), confirm alerts fire on a simulated leaked key.

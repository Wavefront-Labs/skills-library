---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-incident-response
name: cloud-incident-response
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, detection-and-response, cloud-incident-response, ir-playbook, compromised-credentials, containment, nist-sp-800-61, security-incident, key-revocation]
level: advanced
status: draft
description: "Prepare and run cloud security incident response: playbooks for leaked keys, compromised hosts and public data exposure, pre-provisioned IR access, evidence."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.html", "https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://learn.microsoft.com/security/operations/incident-response-playbooks"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud incident response playbook

## Prepare (before anything happens)
- IR roles pre-provisioned in every account (read-only investigation + containment role), usable
  via break-glass if the IdP is compromised.
- Logs centralised and immutable in a separate account; retention ≥ 1 year.
- Forensics account/project with tooling and isolated networking.
- Contact list: provider security/support, legal, comms, data protection officer.

## Playbook: leaked access key / credentials
1. Identify the principal and key; **deactivate** (not delete — keep for evidence) the key;
   revoke sessions (AWS: attach deny policy with `aws:TokenIssueTime` condition / "Revoke active
   sessions"; Entra: revoke refresh tokens; GCP: disable service account key).
2. Query audit logs for all actions by that key since creation: new users/keys/roles, instances
   in unusual regions, data access.
3. Remove persistence (new IAM users, keys, trust policies, Lambda backdoors), terminate attacker resources.
4. Rotate any secrets the principal could read.

## Playbook: compromised instance/container
Isolate (restrictive security group / network policy, remove from LB), snapshot disks and
capture memory if possible, detach the instance role, tag as quarantined, investigate in the
forensics account; replace from clean image.

## Playbook: public data exposure
Block public access, determine exposure window and access logs (S3 server/CloudTrail data
events), assess data classification, engage legal for notification obligations.

## After
Post-incident review, control improvements, update playbooks; run tabletop exercises yearly.

## Verify
- [ ] IR role works in a random account today (test quarterly).
- [ ] Each playbook rehearsed in the last 12 months.

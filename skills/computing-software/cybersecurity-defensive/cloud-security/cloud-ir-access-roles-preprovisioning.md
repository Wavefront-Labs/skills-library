---
id: computing-software.cybersecurity-defensive.cloud-security.cloud-ir-access-roles-preprovisioning
name: cloud-ir-access-roles-preprovisioning
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-incident-response, ir-access-roles, forensics-account, break-glass, aws-organizations, stacksets, ir-readiness]
level: advanced
status: draft
description: "Prepare cloud IR access before you need it: read-only and containment roles in every account, a forensics account, break-glass paths, tooling pre-staged, and regular drills."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/preparation.html", "https://learn.microsoft.com/en-us/security/operations/incident-response-playbooks", "https://cloud.google.com/architecture/framework/security/incident-response"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud IR access roles (preparation)

During an incident you do not want to discover that responders cannot see the affected account, or
that the only admin path runs through the compromised identity provider.

## Roles in every account (AWS example, deployed by StackSets/Control Tower customisations)
- **IR-ReadOnly**: `SecurityAudit` + `ViewOnlyAccess` + read of CloudTrail/Config/VPC flow logs; for triage.
- **IR-Containment**: scoped write actions: modify security groups, detach instance profiles, attach deny
  policies (`AWSDenyAll` inline/quarantine policy), disable access keys, snapshot EBS, isolate instances,
  stop Lambda concurrency, revoke sessions (`iam:PutRolePolicy` for `aws:TokenIssueTime` deny).
- **IR-Forensics**: share snapshots/AMIs to the forensics account, copy logs.
Trust: assumable only from a dedicated security tooling account role, with MFA/SourceIdentity conditions.
Protect them from deletion with SCPs (deny modification of `IR-*` roles except by the security pipeline).

## Forensics account
- Isolated account with no connectivity to production, forensic workstation AMIs (SIFT/REMnux), KMS keys
  that can decrypt shared snapshots (key policy grants in source accounts), evidence S3 bucket with Object
  Lock and versioning, and logging of everything done there.

## Break-glass
- If the IdP (Entra/Okta) is compromised or down: break-glass IAM users or root access procedure with
  hardware MFA, sealed credentials, alerting on use.
- Azure: two emergency access accounts excluded from Conditional Access (with FIDO2), monitored.
- GCP: org-level break-glass with separate super admin.

## Pre-stage tooling and data
- Log availability: org CloudTrail (management + data events for key buckets), VPC flow logs, DNS logs,
  centralised and retained beyond typical dwell time.
- Scripts/runbooks for common containment (AWS IR playbooks, Automated Forensic Orchestrator for EC2).
- Contact list including cloud provider support (enterprise support case with severity "business-critical").

## Drills
Quarterly game day: responder assumes IR roles in a random account, isolates a test instance, snapshots
and shares to forensics, reads CloudTrail. Fix whatever fails.

## Gotchas
- Encrypted snapshots with default AWS managed keys cannot be shared cross-account; use customer managed keys.
- Containment roles that are too broad become an attack path; scope and monitor them like admin.

## Verify
Drill report shows responders completed triage and containment in a random account within the target
time using only pre-provisioned roles.

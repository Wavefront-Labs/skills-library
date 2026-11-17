---
id: computing-software.cybersecurity-defensive.cloud-security.cloud-incident-response
name: cloud-incident-response
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-incident-response, cloudtrail, access-key-compromise, iam-role-compromise, container-escape, serverless-forensics, immutable-infrastructure, snapshot-forensics, blast-radius, aws, azure, gcp]
level: advanced
status: draft
description: "Respond to a cloud incident where there's no host to isolate: compromised access keys/roles, container and serverless forensics, and blast-radius containment across accounts."
sources: ["AWS Security Incident Response Guide (public)", "CrowdStrike/Mandiant public cloud incident response methodology write-ups", "NIST SP 800-61 Rev. 3"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud incident response — there is often no host to isolate

**Goal:** respond to a cloud-native incident (compromised credentials, an
over-permissioned role abused, a container or serverless function compromised)
where the traditional "isolate the endpoint" playbook doesn't directly apply —
the containment unit is usually an identity, a role, or an account, not a box.

## 1. Compromised access keys and roles: revoke the right thing, fast
A leaked long-lived access key or an abused IAM role's temporary credentials is
the single most common cloud incident starting point (keys committed to a public
repo, leaked in a build log, phished from a developer). Immediate actions:
disable/delete the specific access key (not just rotate — a rotated key can still
have active sessions using old temporary credentials derived from it), revoke
active sessions for an assumed role (attach a deny-all policy or use the
provider's session-revocation mechanism — AWS: update the role's trust policy or
apply an explicit deny; this is faster than waiting for temporary credentials to
naturally expire), and check CloudTrail/Activity Log immediately for everything
that identity did, ordered by time, starting from first anomalous use. A
leaked key with 1-hour-lifetime temporary credentials derived from it can still
be active for up to that hour after you revoke the parent — understand your
provider's actual revocation semantics rather than assuming "disabled" is instant
everywhere.

## 2. Reconstruct from the cloud control-plane log, not disk
CloudTrail (AWS), Activity Log (Azure), Cloud Audit Logs (GCP) are the primary
forensic record for a cloud incident — every API call, by whom, from where, is
usually already logged if logging was enabled (verify it was, and wasn't itself
disabled by the attacker as a first move — `CloudTrail:StopLogging` or
equivalent is itself a very high-confidence indicator). Pull the full timeline
of API calls from the compromised identity: what was enumerated (reconnaissance:
`List*`/`Describe*` calls), what was created (persistence: new IAM users/roles/
access keys, new Lambda functions, new EC2 instances in unexpected regions), and
what was exfiltrated (data access, snapshot/AMI sharing to an external account,
S3 object reads at volume).

## 3. Container and serverless forensics: capture before it disappears
A compromised container or serverless function (Lambda, Cloud Functions) may be
destroyed/replaced by the orchestrator or auto-scaling within minutes — there is
often no persistent disk to image after the fact. Capture immediately: the
running container's filesystem/logs (`docker commit`/`kubectl cp`/export before
termination, or at minimum centralized logs if shipped elsewhere already),
environment variables and mounted secrets (common injection/persistence point),
and the image/function version deployed (compare against the last known-good
build artifact in CI to spot a supply-chain or build-pipeline compromise). Treat
the underlying image registry/build pipeline as potentially compromised too if
multiple instances show the same symptom — the attacker may have poisoned the
image, not just exploited one running instance.

## 4. Blast-radius containment across accounts
Cloud environments are often multi-account (AWS Organizations, Azure
subscriptions, GCP projects linked via shared VPCs, cross-account roles, shared
CI/CD). A compromised identity in one account may be able to assume roles into
others — pull the compromised identity's effective permissions including any
cross-account `AssumeRole`/federation trust, and check activity in *every*
account reachable that way, not just the one where the incident was detected.

## 5. Snapshot before remediating; preserve immutably
Cloud makes evidence preservation cheap: snapshot the affected
volumes/disks, export the relevant logs to a separate, access-restricted
account/bucket with object lock/immutability enabled, before terminating or
rebuilding the affected resources. This is both faster and more reliable than
on-prem disk imaging, if you remember to do it before tearing down.

## Gotchas
- "Rotate the key" alone is not containment if an attacker already created a
  second, persistent access key, IAM user, or role on the compromised identity's
  permissions — always check for and remove every new credential/identity object
  created during the window, not just the one that leaked.
- Logging disabled by the attacker (or never enabled) leaves zero CloudTrail-
  equivalent record — verify logging coverage across all regions/services (some
  providers require explicit per-region trail configuration) as a standing
  control, not just during an incident.
- Terminating a compromised instance/container before capturing logs/state loses
  evidence that cloud snapshot tooling could have preserved cheaply.
- Assuming the blast radius stops at the account where detection happened misses
  cross-account pivots via trust relationships — map them explicitly.

## Verify
- [ ] The compromised credential/role's full activity timeline was pulled from
      the control-plane log before or immediately after revocation.
- [ ] Logging coverage (all regions/services) was confirmed active for the
      incident window, not assumed.
- [ ] Any new credentials/identities created by the attacker were found and removed.
- [ ] Cross-account trust relationships from the compromised identity were
      checked for pivot activity.
- [ ] Snapshots/log exports were taken to an immutable, separate location before
      remediation/teardown.

Related: computing-software.cybersecurity-defensive.cloud-security.cspm-and-least-privilege-remediation,
computing-software.cybersecurity-defensive.security-operations.incident-response-coordination,
computing-software.cybersecurity-defensive.identity-access-management.identity-threat-detection

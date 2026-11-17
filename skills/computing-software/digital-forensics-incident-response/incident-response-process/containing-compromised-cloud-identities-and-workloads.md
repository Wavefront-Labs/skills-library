---
id: computing-software.digital-forensics-incident-response.incident-response-process.containing-compromised-cloud-identities-and-workloads
name: containing-compromised-cloud-identities-and-workloads
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [cloud-containment, containment, aws, azure, gcp, iam, cloud-incident-response, dfir]
level: advanced
status: docs-checked
description: "Contain compromised cloud identities and workloads in AWS, Entra and GCP: key deactivation, session and token revocation, and snapshot-then-isolate for instances."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html", "https://learn.microsoft.com/en-us/entra/identity/users/users-revoke-access", "https://learn.microsoft.com/en-us/powershell/module/microsoft.graph.users.actions/revoke-mgusersigninsession", "https://cloud.google.com/architecture/framework/security"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Containing compromised cloud identities and workloads

**Goal:** stop the attacker using cloud credentials and compute, preserving evidence (logs,
snapshots) before deleting anything.

## AWS
```bash
# Leaked access key
aws iam update-access-key --user-name app-ci --access-key-id <KEY_ID> --status Inactive
# Isolate an EC2 instance (keep running for memory capture)
aws ec2 modify-instance-attribute --instance-id <INSTANCE_ID> --groups <ISOLATION_SG>
aws ec2 create-snapshot --volume-id <VOLUME_ID> --description "IR-2026-014 EVID-021"
```
- Kill existing role sessions: in the IAM console choose the role, then Revoke sessions, Revoke active sessions. IAM
  attaches an inline policy named `AWSRevokeOlderSessions` that denies all actions for sessions assumed before now
  plus about 30 seconds. You need `PutRolePolicy`; it hits every user of the role (a warning on the page), cannot be
  done for a service-linked role, and sessions created later are unaffected. Roles created from IAM Identity Center
  permission sets cannot be edited in IAM: revoke the permission set session in IAM Identity Center instead.
- The CLI-based form is a policy with a `DateLessThan` condition on `aws:TokenIssueTime`; the value exists only on
  requests signed with temporary credentials, so it does not stop an IAM user's long-term keys (deactivate those).
  The AWS CLI caches credentials until they expire and may need its cache cleared.
- Also check for attacker-created IAM users, keys, roles and Lambda functions (see aws-incident-response).

## Azure / Entra
- Disable the user or service principal; `Revoke-MgUserSignInSession -UserId $User.Id` revokes the user's Entra
  refresh tokens. Access tokens are valid for 1 hour by default, so the user may keep access until they expire unless the
  application supports Continuous Access Evaluation (CAE).
- Remove credentials (secrets, certificates) added to app registrations.
- Review role assignments created during the incident in the Activity log. Snapshot VM disks and restrict VM
  network access per your platform's documentation.

## GCP
```bash
gcloud iam service-accounts keys disable KEY_ID --iam-account sa@proj.iam.gserviceaccount.com
gcloud iam service-accounts disable sa@proj.iam.gserviceaccount.com
gcloud compute instances add-tags vm1 --tags quarantine   # with a deny-all firewall rule on that tag
gcloud compute disks snapshot vm1-disk --snapshot-names ir-evid-030
```

## Gotchas
- Attackers create backup access (new users, keys, federated IdP trust, cross-account roles):
  enumerate IAM changes in the audit log for the whole incident window before declaring
  containment.
- Deleting resources destroys evidence; snapshot and tag first.

## Verify
CloudTrail / Activity log / Cloud Audit Logs show only denied calls from the compromised
principal after the containment time.

## Checked
2026-11-08. Confirmed: IAM revoke-sessions page (AWSRevokeOlderSessions behaviour, PutRolePolicy, limits,
aws:TokenIssueTime, CLI cache); Entra "Revoke user access" page and Revoke-MgUserSignInSession page (refresh token
revocation, 1-hour default access token lifetime, CAE); gcloud and aws commands and flags (check_commands.py). Removed
(unconfirmed): the SCP and org-policy containment note, instance termination protection and instance profile steps,
the NSG specifics, and the exact Activity log operation name for role assignments. The GCP framework source covers
only general guidance.
Method: documentation only; no commands were run.

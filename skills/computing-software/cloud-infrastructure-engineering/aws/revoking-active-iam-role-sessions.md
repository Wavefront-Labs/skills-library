---
id: computing-software.cloud-infrastructure-engineering.aws.revoking-active-iam-role-sessions
name: revoking-active-iam-role-sessions
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, sts, revoke-sessions, tokenissuetime, incident-response, compromised-credentials-role, iam-role]
level: advanced
status: docs-checked
description: "Kill stolen temporary credentials: revoke active role sessions with an aws:TokenIssueTime deny, target one session by source identity or IP, and clean up after."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_disable-perms.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/revoke-user-permissions.html", "https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-iam.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Revoking active role sessions

**Problem:** temporary credentials (role sessions, Identity Center sessions, instance
profile creds) cannot be deleted. Once leaked they are valid until expiry, up to 12 hours
for role sessions (36 hours for `GetSessionToken` and `GetFederationToken`). The fix is an explicit
deny keyed on when the token was issued. You cannot revoke the session of a service-linked role.

## 1. Console button (fast path)
IAM, Roles, the role, **Revoke sessions** tab, *Revoke active sessions*. It attaches an
inline policy named `AWSRevokeOlderSessions`:
```json
{"Version": "2012-10-17",
 "Statement": [{"Effect": "Deny", "Action": ["*"], "Resource": ["*"],
   "Condition": {"DateLessThan": {"aws:TokenIssueTime": "2026-10-18T09:41:00Z"}}}]}
```
Every session issued before that timestamp (plus about 30 seconds into the future, for policy propagation)
now fails every call; sessions created later work. The AWS CLI caches credentials, so clear its cache to force
a refresh.

## 2. CLI equivalent
```bash
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
aws iam put-role-policy --role-name AppRole --policy-name AWSRevokeOlderSessions \
  --policy-document "{\"Version\":\"2012-10-17\",\"Statement\":[{\"Effect\":\"Deny\",\"Action\":\"*\",\"Resource\":\"*\",\"Condition\":{\"DateLessThan\":{\"aws:TokenIssueTime\":\"$NOW\"}}}]}"
```
Re-running updates the timestamp (the console also updates the existing policy).

## 3. Narrower revocation
Revoking everything also breaks healthy instances and tasks using the role until they
obtain new credentials. To hit only the attacker:
- By source IP: `"NotIpAddress": {"aws:SourceIp": ["203.0.113.0/24"]}` plus
  `"Bool": {"aws:ViaAWSService": "false"}` so service-made calls still work.
- By VPC: deny when `aws:SourceVpc` is not yours (calls through VPC endpoints carry it).
- By session: `"StringEquals": {"aws:userid": "AROAEXAMPLEID:i-0abc123"}` or by
  `aws:SourceIdentity` for a specific human.
- EC2 credential exfiltration specifically: the `aws:Ec2InstanceSourceVpc` and
  `aws:Ec2InstanceSourcePrivateIPv4` condition keys let you deny instance-profile creds used from
  anywhere other than the instance they were issued to.

## 4. Identity Center and federated users
- Identity Center: you cannot edit the roles created from permission sets in IAM. Follow the
  Identity Center user guide procedure "Revoke user access": a deny-all SCP naming the user ID, removal of
  the user's assignments, deleting their portal session, disabling the user, and leaving the deny in place
  for at least 12 hours.
- IAM users: deactivate access keys (`aws iam update-access-key --status Inactive`);
  sessions from `GetSessionToken` derived from them still need the TokenIssueTime deny
  attached to the **user**.

## 5. Order of operations in an incident
1. Attach the revoke policy (stop the bleeding).
2. Find the leak: CloudTrail for the role's `accessKeyId` values, `sourceIPAddress`, and
   user agents; GuardDuty findings `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS`
   and `.InsideAWS`.
3. Remove the root cause (rotate the secret, patch the SSRF, enforce IMDSv2).
4. After the maximum session duration has passed since the revoke timestamp, delete
   the inline policy so it does not confuse later debugging.

## Gotchas
- The revoke policy is a Deny on `*`, so it also blocks the console role you use to
  investigate if you are using the same role. Use a separate incident role.
- SCPs or permission boundaries do not help here; the deny must be on the role (or an
  SCP keyed on TokenIssueTime, which is valid org-wide for mass events).
- Service-linked roles cannot be revoked this way; open an AWS Support case if one is implicated.

## Verify
- [ ] A session minted before the timestamp gets `AccessDenied ... explicit deny in an identity-based policy` on a test call such as `aws s3 ls`.
- [ ] A freshly assumed session works.
- [ ] Workloads using the role recovered after credential refresh; CloudTrail shows no further calls from the attacker IP.
- [ ] Inline revoke policy removed after max session duration elapsed.

## Checked

Checked 2026-10-27 against the IAM User Guide pages "Revoke IAM role temporary security credentials", "Disabling permissions for temporary security credentials" and the global condition keys page, the IAM Identity Center page "Revoke user access", the GuardDuty IAM finding types page and the STS GetSessionToken reference:
- The `AWSRevokeOlderSessions` inline policy, the `aws:TokenIssueTime` condition, the roughly 30 second look-ahead, CLI cache, and that service-linked role sessions cannot be revoked.
- IAM cannot edit Identity Center permission set roles; the Identity Center procedure is SCP and assignment based.
- Condition keys `aws:SourceIp`, `aws:SourceVpc`, `aws:ViaAWSService`, `aws:Ec2InstanceSourceVpc` and `aws:Ec2InstanceSourcePrivateIPv4` exist; GuardDuty finding names end in `.InsideAWS` and `.OutsideAWS`.
Removed: the SDK refresh timing claim and the earlier Identity Center advice. The commands were not run.

Method: documentation only; no commands were run.

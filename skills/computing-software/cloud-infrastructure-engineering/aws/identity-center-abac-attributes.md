---
id: computing-software.cloud-infrastructure-engineering.aws.identity-center-abac-attributes
name: identity-center-abac-attributes
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam-identity-center, identity-center, sso, abac, identity-center-abac, attributes-for-access-control, session-tags, principaltag, saml-attributes, scim, permission-sets]
level: advanced
status: docs-checked
description: "Use IAM Identity Center attributes for access control: map directory or SAML attributes to session tags and write permission sets that scope access by aws:PrincipalTag."
sources: ["https://docs.aws.amazon.com/singlesignon/latest/userguide/abac.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/configure-abac.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/attributemappingsconcept.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identity Center ABAC with user attributes

**Goal:** one permission set (e.g. `ProjectDeveloper`) serves every team, and what each user
can touch is decided by an attribute from the directory (`project`, `costCenter`,
`department`) matched against resource tags, instead of one permission set per team.

## 1. Turn on attributes for access control
Console: IAM Identity Center → Settings → *Attributes for access control* → Enable, then add
key → value-source mappings. CLI (management or delegated admin account):
```bash
INSTANCE=$(aws sso-admin list-instances --query 'Instances[0].InstanceArn' --output text)
aws sso-admin create-instance-access-control-attribute-configuration --instance-arn $INSTANCE \
  --instance-access-control-attribute-configuration '{"AccessControlAttributes":[
    {"Key":"project","Value":{"Source":["${path:enterprise.department}"]}},
    {"Key":"costcenter","Value":{"Source":["${path:enterprise.costCenter}"]}}]}'
```
- Sources use Identity Center attribute paths (`${path:...}`) for users synced by SCIM or
  created in the Identity Center directory.
- An external IdP can instead send attributes in the SAML assertion as
  `https://aws.amazon.com/SAML/Attributes/AccessControl:<Key>`. If the same key is also
  defined as an access-control attribute in Identity Center, Identity Center sends the value
  from its identity store as the session tag. Attributes that only the IdP sends do not show
  on the console's Attributes for access control page.
- Each key becomes a **session tag** on the role session that the permission set creates.

## 2. Permission set policy
```json
{"Version":"2012-10-17","Statement":[
 {"Effect":"Allow","Action":["ec2:StartInstances","ec2:StopInstances","ec2:RebootInstances"],
  "Resource":"*","Condition":{"StringEquals":{"aws:ResourceTag/project":"${aws:PrincipalTag/project}"}}},
 {"Effect":"Allow","Action":["ec2:Describe*"],"Resource":"*"},
 {"Effect":"Allow","Action":["s3:GetObject","s3:PutObject"],
  "Resource":"arn:aws:s3:::data-${aws:PrincipalTag/project}/*"},
 {"Effect":"Allow","Action":"ec2:CreateTags","Resource":"*",
  "Condition":{"StringEquals":{"aws:RequestTag/project":"${aws:PrincipalTag/project}","ec2:CreateAction":["RunInstances","CreateVolume"]}}},
 {"Effect":"Deny","Action":["ec2:CreateTags","ec2:DeleteTags"],"Resource":"*",
  "Condition":{"ForAnyValue:StringEquals":{"aws:TagKeys":["project"]},"Null":{"ec2:CreateAction":"true"}}}
]}
```
The last two statements matter: users may set the `project` tag only to their own value at
create time, and may never retag an existing resource into their project.

## 3. Make the tags trustworthy
- Attribute changes in the IdP flow via SCIM; the user gets the new tag at next sign-in /
  session. Sessions already issued keep the old tags until they expire, so keep session
  duration modest for ABAC permission sets.
- Lock who can edit those attributes in the IdP (HR-sourced, not self-service).
- Enforce resource tagging (tag policy + SCP) or ABAC grants nothing on untagged resources,
  which looks like random `AccessDenied`.

## Gotchas
- A new session tag overrides an existing one with the same key regardless of character
  case; pick one lowercase convention for keys and enforce it with a tag policy.
- An empty attribute means the session has no such tag; `${aws:PrincipalTag/project}` then
  fails to match anything (fail closed). Good, but surface it in onboarding docs.
- Not every service supports `aws:ResourceTag` for every action; check the service
  authorization reference before promising ABAC for that service.
- Session tags add to the session token size; if the token exceeds the limit the call
  returns an error that reports the size (`SessionTokenUtilization` shows the percentage
  used). A session can carry at most 50 session tags.
- AWS STS does not support multi-valued session tags: pass one value per key.

## Verify
- [ ] Sign in as a user with `department=alpha`; the CloudTrail event for the role session shows the `project=alpha` principal tag.
- [ ] Starting an instance tagged `project=beta` is denied; `project=alpha` is allowed.
- [ ] Retagging an `alpha` resource to `beta` is denied.
- [ ] Change the attribute in the IdP, wait for SCIM sync, sign in again: access follows.

## Checked

Checked 2026-10-27 against the IAM Identity Center User Guide (ABAC, Enable and configure attributes for access control, Attribute mappings) and the IAM User Guide page on session tags:
- `${path:enterprise.department}` and `${path:enterprise.costCenter}` are listed as supported attribute paths.
- If an attribute is defined both in a SAML assertion and in Identity Center, Identity Center's identity store value is sent as the session tag.
- The `https://aws.amazon.com/SAML/Attributes/AccessControl:<TagKey>` name format appears in the Okta setup page.
- Session tags: single value per key only, maximum 50, count toward token size, new tags override same-key tags regardless of case, principal tags are visible in CloudTrail.
- `create-instance-access-control-attribute-configuration` takes an instance ARN and a list of attributes (Key, Value.Source with exactly one source) in the botocore sso-admin model; the list holds at most 50 entries.
The example permission-set policy is IAM policy logic and was not evaluated.

Method: documentation only; no commands were run.

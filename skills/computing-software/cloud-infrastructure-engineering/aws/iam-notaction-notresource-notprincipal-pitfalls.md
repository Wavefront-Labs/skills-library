---
id: computing-software.cloud-infrastructure-engineering.aws.iam-notaction-notresource-notprincipal-pitfalls
name: iam-notaction-notresource-notprincipal-pitfalls
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam, notaction, notresource, notprincipal, deny-statements, policy-review, least-privilege]
level: advanced
status: docs-checked
description: "Use NotAction, NotResource and NotPrincipal safely: pair them with Deny, avoid accidental admin grants, and replace NotPrincipal with aws:PrincipalArn conditions."
sources: ["https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notaction.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notresource.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_variables.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notprincipal.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws_deny-requested-region.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_aws_my-sec-creds-self-manage.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html", "https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NotAction, NotResource, NotPrincipal: when and how
**Goal:** write the negated elements only where they shrink a policy safely, and spot the
ones in a review that quietly grant far more than intended.

## 1. The rule of thumb
- **`Not*` with `Deny`** = "deny everything except X". Safe and common.
- **`NotAction` with `Allow`** = "allow everything that is not listed". The IAM guide warns that it matches all
  services and actions not explicitly listed (or not applicable to the resource), which can grant more than you
  intended, including actions in services launched later. Use it only with a narrow `Resource`.

## 2. NotAction
Good: force MFA for everything except the calls needed to set it up (from the AWS self-service example).
```json
{"Sid": "DenyAllExceptMfaSetupWithoutMfa", "Effect": "Deny",
 "NotAction": ["iam:CreateVirtualMFADevice", "iam:EnableMFADevice", "iam:GetUser",
               "iam:GetMFADevice", "iam:ListMFADevices", "iam:ListVirtualMFADevices",
               "iam:ResyncMFADevice", "sts:GetSessionToken"],
 "Resource": "*",
 "Condition": {"BoolIfExists": {"aws:MultiFactorAuthPresent": "false"}}}
```
A `Deny` with `NotAction` does not allow anything: if the user is signed in with MFA the condition test fails and
the statement has no effect, so other policies still have to grant the permissions.
Good: region lock, exempting global services (the AWS example for denying access based on the requested Region).
```json
{"Effect": "Deny",
 "NotAction": ["cloudfront:*", "iam:*", "organizations:*", "route53:*", "support:*"],
 "Resource": "*",
 "Condition": {"StringNotEquals": {"aws:RequestedRegion": ["eu-central-1", "eu-west-1"]}}}
```
The AWS page says to edit the `NotAction` list for other global services you use (it names `budgets`,
`globalaccelerator`, `importexport` and `waf` as examples) and notes that some global services have endpoints in
`us-west-2`; take the current list from that page.
Bad: "power user minus IAM".
```json
{"Effect": "Allow", "NotAction": "iam:*", "Resource": "*"}
```
This is the form the IAM guide shows for "every action in every service except IAM"; it grants every non-IAM
action in every current and future service, so treat it as an admin-equivalent grant and prefer an explicit
allow-list.

## 3. NotResource
Good: deny every S3 resource except the listed ones (the shape of the IAM guide's payroll example).
```json
{"Effect": "Deny", "Action": "s3:*",
 "NotResource": ["arn:aws:s3:::upload-inbox", "arn:aws:s3:::upload-inbox/*"]}
```
New buckets are automatically denied unless you add them to `NotResource`. The listed resources are the only ones
not limited, so every resource that applies to the statement's actions is denied; keep `Action` to one service,
because adding actions from another service would deny that service's resources too. This statement grants nothing.
Bad: `Allow` + `NotResource`. The guide says never to combine `"Effect": "Allow"`, `"Action": "*"` and
`NotResource` (it allows everything except the listed resource, even letting a user add a policy to
themselves), and to be careful with `Allow` + `NotResource` generally because it allows all services and
resources not explicitly listed. Instead, deny the sensitive resource explicitly and allow a named list.
If a policy variable has no value in the request, a `Resource` or `NotResource` containing it matches no resource,
so test negated resources that use variables.

## 4. NotPrincipal (resource policies)
`NotPrincipal` must be used with `"Effect": "Deny"` (with Allow it is not supported). It works in resource-based
policies of some services, not in identity-based policies or role trust policies, and not in SCPs or RCPs. AWS does
not recommend it for new resource-based policies because troubleshooting across policy types is hard.
```json
{"Effect": "Deny", "NotPrincipal": {"AWS": ["arn:aws:iam::111122223333:role/App", "arn:aws:iam::111122223333:root"]},
 "Action": "s3:*", "Resource": ["arn:aws:s3:::secret", "arn:aws:s3:::secret/*"]}
```
Problems:
- You must also list the account ARN of the not-denied principal, or the policy might deny the whole account;
  for assumed-role sessions AWS may validate the account, then the role, then the session, so list the role ARN and
  the account.
- A `NotPrincipal` + `Deny` statement always denies any IAM principal that has a permissions boundary attached,
  whatever you list, so principals with boundaries lose access.
Preferred form (the AWS-recommended alternative, using `aws:PrincipalArn` with an ARN operator):
```json
{"Effect": "Deny", "Principal": "*", "Action": "s3:*",
 "Resource": ["arn:aws:s3:::secret", "arn:aws:s3:::secret/*"],
 "Condition": {"ArnNotEquals": {"aws:PrincipalArn": [
   "arn:aws:iam::111122223333:role/App",
   "arn:aws:iam::111122223333:role/BreakGlass"]}}}
```
For IAM roles `aws:PrincipalArn` returns the ARN of the role, not of the user that assumed it or the session; do
not use an assumed-role session ARN as its value.

## 5. Finding them in an account
Review every `Allow` statement with `NotAction` or `NotResource` in customer managed and inline policies; the
`get-account-authorization-details` output lists all policy documents for an account-wide review.

## Gotchas
- `NotAction` on a Deny that lacks a condition denies every other action, including the console calls
  (`iam:GetUser`) users need to see their own account.
- Global services in a region-deny list change over time; review the exemption list when an SCP blocks a
  legitimate console page.

## Verify
- [ ] No `Allow` statement in customer policies uses `NotAction` or `NotResource` unless it is documented as an admin-equivalent grant.
- [ ] Every `NotPrincipal` in resource policies replaced by `aws:PrincipalArn` conditions; a test session of the allowed role still works.
- [ ] Policy simulator confirms the Deny-with-NotAction statement blocks a sample excluded action and permits the exempt ones.

## Checked
Checked 2026-10-24 against the IAM User Guide pages for NotAction, NotResource, NotPrincipal, policy variables, the deny-by-Region example,
the MFA self-service example, global condition keys and permissions boundaries. Corrected: the old text called
`Allow` + `NotAction` "almost always an over-grant" and said the role ARN does not match its session principal
so both must be listed; the guide says to be careful with `NotAction`+`Allow` and to list the role ARN together
with the account ARN, and it recommends `aws:PrincipalArn` with `ArnNotEquals`. The old MFA exemption list was
missing `iam:GetMFADevice`. The Region-lock exemption list now matches the AWS example (the old list added
`sts:*`, `budgets:*`, `globalaccelerator:*` and `waf:*` as if standard). Added the permissions boundary
interaction from the NotPrincipal and boundaries pages. Removed the `jq` pipeline over
`get-account-authorization-details`, the claim that Access Analyzer warns on `Allow`+`NotAction`, and the
wildcard-in-`NotAction` and mixed `NotAction`/`NotResource` logic notes, which were not confirmed, and rewrote the
NotResource section to the guide's Deny example and its warnings about `Allow`.
Method: documentation only; no commands were run.

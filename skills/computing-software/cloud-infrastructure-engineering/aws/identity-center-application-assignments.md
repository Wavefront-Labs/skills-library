---
id: computing-software.cloud-infrastructure-engineering.aws.identity-center-application-assignments
name: identity-center-application-assignments
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, iam-identity-center, identity-center, sso, application-assignments, customer-managed-application, aws-managed-application, saml-application, oauth-application, trusted-identity-propagation, trusted-token-issuer, identity-enhanced-session]
level: advanced
status: docs-checked
description: "Assign users and groups to Identity Center applications: custom SAML/OAuth apps, AWS managed apps, assignment-required settings and trusted identity propagation to data services."
sources: ["https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-applications.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/awsapps.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/awsapps-that-work-with-identity-center.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/customermanagedapps.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/trustedidentitypropagation-overview.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/using-apps-with-trusted-token-issuer.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/trustedidentitypropagation-identity-enhanced-iam-role-sessions.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-considerations.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identity Center application assignments

**Goal:** the access portal shows each user the business apps (SAML/OAuth) and AWS apps
(for example Amazon Quick, Amazon Q Business, Amazon Redshift, Amazon Athena SQL, SageMaker
Unified Studio, S3 Access Grants) they are entitled to, assigned by group, and data services see the
real user identity rather than only a shared role.

## 1. Two kinds of application
| | Customer managed | AWS managed |
|---|---|---|
| Examples | Salesforce, Jira, internal app via SAML 2.0 or OAuth 2.0 | Amazon Quick, Amazon Q Business, Amazon Redshift, AWS Lake Formation, Amazon S3 Access Grants, Amazon EMR Studio |
| Created by | You in Identity Center | The AWS service, when you connect it to the Identity Center instance |
| Assignment | Users/groups in Identity Center | Assignments are required by default; the application separately controls access to its own resources |

## 2. Customer managed SAML app
1. Identity Center → Applications → Add → *I have an application I want to set up* → SAML 2.0.
2. Exchange metadata: give the app the Identity Center SAML metadata/IdP URL; enter the
   app's ACS URL and audience (SP entity ID).
3. Attribute mappings: `Subject` → `${user:email}` (format `emailAddress`) or the immutable
   `${user:subject}`; add `groups`/role attributes the app expects.
4. Assign groups:
```bash
aws sso-admin list-applications --instance-arn $INSTANCE
aws sso-admin create-application-assignment --application-arn <APP_ARN> \
  --principal-id <GROUP_ID> --principal-type GROUP
aws sso-admin put-application-assignment-configuration --application-arn <APP_ARN> --assignment-required
```
`--assignment-required` (or `--no-assignment-required`) controls whether only assigned
principals can sign in. For a portal-launched app keep it required.

## 3. Trusted identity propagation (TIP)
TIP passes the signed-in user's identity (not just the IAM role) to AWS data services, so
Lake Formation grants, S3 Access Grants and Redshift permissions can be per user/group and
CloudTrail shows `onBehalfOf` the user.
- AWS managed app path: enable the integration in each service (e.g. Redshift IdC
  application, Lake Formation IdC integration, S3 Access Grants instance associated with
  the Identity Center instance) and assign groups there.
- Your own app with an external OIDC IdP: register a **trusted token issuer**
  (`aws sso-admin create-trusted-token-issuer --trusted-token-issuer-type OIDC_JWT ...`),
  create a customer managed OAuth application with a JWT-bearer grant
  (`put-application-grant`), exchange the IdP token at the Identity Center OIDC
  `CreateTokenWithIAM` API, then call `sts:AssumeRole` with the user's `userId` context assertion in
  `ProvidedContexts` (provider `arn:aws:iam::aws:contextProvider/IdentityCenter`) to get an
  *identity-enhanced* role session.

## Gotchas
- Group assignments only work for groups that exist in Identity Center (synced via SCIM or
  local). A group present only in the IdP SAML claim is invisible to assignments.
- Application assignment is separate from AWS account assignment (permission sets). Users
  frequently have one and expect the other.
- Changing the identity source to Active Directory (from the Identity Center directory, an
  external IdP, or another AD) removes users, groups, memberships and assignments; changing
  between the Identity Center directory and external IdPs preserves them. Export first anyway.
- Every AWS managed app integrates with the organization instance; only some also work with
  account instances, support trusted identity propagation, or deploy in additional Regions.
  Check the managed-application table. Customer managed SAML 2.0 apps need an organization instance.
- SAML `Subject` changes (e.g. email to subject ID) orphan accounts in the target app.

## Verify
- [ ] An assigned user sees the tile in the access portal and lands signed-in in the app.
- [ ] An unassigned user gets a "not assigned" error when `assignment-required` is set.
- [ ] `list-application-assignments --application-arn <APP_ARN>` matches the intended groups.
- [ ] For TIP: CloudTrail data event on S3/Redshift/Lake Formation shows the user identity (`onBehalfOf` with `userId` and `identityStoreArn`; not every service logs it), and a user outside the granted group is denied.

## Checked

Checked 2026-10-27 against the IAM Identity Center User Guide pages on AWS managed applications (and the managed-application table), customer managed applications, identity-enhanced IAM role sessions, trusted token issuers and instance types, plus the botocore sso-admin model:
- Operations `create-application-assignment`, `put-application-assignment-configuration` (boolean `AssignmentRequired`), `create-trusted-token-issuer` (type `OIDC_JWT`) and `put-application-grant` (grant type `urn:ietf:params:oauth:grant-type:jwt-bearer`) exist.
- The identity-enhanced session flow (CreateTokenWithIAM id token, then AssumeRole with `ProvidedContexts`) and the CloudTrail `onBehalfOf` element are as documented.
- Application names in the table match the managed-application list; assignments are required by default for AWS managed applications.
- Identity source change behaviour is as stated on the considerations page.
The CLI examples were not run.

Method: documentation only; no commands were run.

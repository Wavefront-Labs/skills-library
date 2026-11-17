---
id: computing-software.cloud-infrastructure-engineering.aws.identity-center-external-idp-and-scim
name: identity-center-external-idp-and-scim
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, identity-center, external-idp, scim, entra-id, okta, saml, user-provisioning, identity-source]
level: practitioner
status: docs-checked
description: "Connect IAM Identity Center to Entra ID or Okta: SAML metadata exchange, SCIM automatic provisioning with access tokens, group sync, attribute mapping and token rotation."
sources: ["https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-identity-source-idp.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/provision-automatically.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/idp-microsoft-entra.html", "https://docs.aws.amazon.com/singlesignon/latest/userguide/gs-okta.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Identity Center with an external IdP and SCIM

**Goal:** people log in with corporate credentials and MFA; joiners/leavers flow
automatically; AWS access is driven by IdP groups.

## 1. Switch identity source (SAML)
Identity Center → Settings → Identity source → External identity provider:
1. Download Identity Center's SAML metadata (ACS URL, issuer) → create an enterprise app in
   Entra ID ("AWS IAM Identity Center" gallery app) or Okta ("AWS IAM Identity Center" app).
2. Upload the IdP's metadata XML to Identity Center.
3. NameID: user principal/email — must match the `userName` SCIM will create.
Changing between the Identity Center directory and an external IdP (or between two external
IdPs) preserves users, groups, memberships and assignments; changing to Active Directory removes
them. Export your configuration and test with a pilot first.

## 2. Enable SCIM provisioning
Identity Center → Enable automatic provisioning → copy **SCIM endpoint** and **access
token** into the IdP app's provisioning settings.
- Entra ID: Provisioning mode Automatic, assign *groups* to the app and scope provisioning to assigned
  users and groups.
- Okta: enable Push Groups for the groups you assign.
- Attribute mapping: follow the attribute lists on the Entra ID and Okta setup pages and the
  supported-attribute table; unsupported mappings cause SCIM errors.

## 3. Token rotation
SCIM access tokens are valid for **1 year**. When a token expires in 90 days or less, the console
and the AWS Health Dashboard send reminders. Generate a new token, update the IdP, then delete
unused or expired tokens. Put the expiry in the calendar: once a token expires, synchronization
from the IdP stops, so creates, updates and deletes no longer arrive.

## 4. Operations
```bash
aws identitystore list-users --identity-store-id d-xxxx --filters AttributePath=UserName,AttributeValue=jo@example.com
aws identitystore list-group-memberships-for-member --identity-store-id d-xxxx --member-id UserId=<ID>
```
Active portal sessions end at session expiry (configure session duration in Identity Center settings);
ending a portal session does not end role sessions already issued.

## Gotchas
- Entra ID provisioning cannot read users in nested groups: only immediate members of an
  explicitly assigned group are provisioned; flatten groups in the IdP.
- Prefer users and groups managed by the IdP; edits made in Identity Center can be overwritten
  during synchronization. Reference group IDs in IaC.

## Verify
- [ ] Assigning a new user to the AWS group in the IdP → user appears in Identity Center within one cycle and can log in.
- [ ] Removing them in the IdP removes the user's access once the change syncs and existing sessions expire.
- [ ] SCIM token expiry date recorded with a renewal reminder well before the 90-day reminder window ends.

## Checked

Checked 2026-10-27 against the IAM Identity Center User Guide pages on automatic provisioning (SCIM), the Microsoft Entra ID setup page, the Okta setup page and considerations for changing the identity source:
- SCIM token validity one year, reminders from 90 days, expired token stops synchronization.
- Entra ID cannot provision users in nested groups; Okta uses Push Groups; SAML attribute name format on the setup pages.
- Identity source change behaviour.
Removed because no page confirmed them: the provisioning cycle length, the number of tokens that can exist, required attribute list, group-name uniqueness and deprovisioning behaviour. The CLI examples were not run.

Method: documentation only; no commands were run.

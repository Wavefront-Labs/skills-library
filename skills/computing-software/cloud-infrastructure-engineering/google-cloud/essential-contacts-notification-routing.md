---
id: computing-software.cloud-infrastructure-engineering.google-cloud.essential-contacts-notification-routing
name: essential-contacts-notification-routing
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, essential-contacts, notifications, security-notifications, org-policy, governance]
level: practitioner
status: docs-checked
description: "Route Google's security, billing, legal and suspension notices to team mailboxes with Essential Contacts at org, folder and project level, and restrict contact domains."
sources: ["https://cloud.google.com/resource-manager/docs/managing-notification-contacts", "https://cloud.google.com/sdk/gcloud/reference/essential-contacts/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Essential Contacts

**Problem:** without custom contacts, notifications in a category go to fallback contacts chosen by
IAM role, who may have left the company or may not be the right team. Essential Contacts is a
directory only: it does not send email itself, and not every Google Cloud product uses it.

## 1. Categories
API/`gcloud` values: `all`, `billing`, `legal`, `product-updates`, `security`, `suspension`, `technical`,
`technical-incidents`. `all` is a superset of billing, legal, product updates, security, suspension and
technical. Contacts are inherited through the resource hierarchy (org contacts cover every folder and
project below).

Google's recommendation: billing, legal and security at the organization (security at project level
if project owners run their own security); product updates, suspension, technical and all at folder or
project level, because technical contacts can receive many notifications.

## 2. Set them at the top
```bash
gcloud essential-contacts create --organization=<ORG_ID> \
  --email=gcp-security@example.com --notification-categories=security,suspension,technical-incidents --language=en
gcloud essential-contacts create --organization=<ORG_ID> \
  --email=finops@example.com --notification-categories=billing --language=en
gcloud essential-contacts create --organization=<ORG_ID> \
  --email=legal-cloud@example.com --notification-categories=legal --language=en
gcloud essential-contacts create --folder=<TEAM_FOLDER> \
  --email=team-payments@example.com --notification-categories=technical,product-updates --language=en
```
`--email`, `--language` (ISO 639-1 code) and `--notification-categories` are required. Use **group
mailboxes** or distribution lists, never individuals.

## 3. Check what a project actually gets
```bash
gcloud essential-contacts compute --project=<P> --notification-categories=security
gcloud essential-contacts list --organization=<ORG_ID>
```

## 4. Lock the domain and security contacts
- Org policy `constraints/essentialcontacts.allowedContactDomains` (list; values like `@example.com`)
  limits which email domains can be added. It does not affect updating or removing existing contacts.
- `essentialcontacts.managed.allowedContactDomains` is the managed-constraint variant.
- Boolean `constraints/essentialcontacts.disableProjectSecurityContacts` blocks project-level contacts
  that subscribe to `SECURITY` or `ALL`, so only org/folder contacts receive security notices.

## Gotchas
- Contacts you have not validated in the past year may prompt for verification in the console; an
  unvalidated contact keeps receiving notifications unless its address is invalid or removed.
- Google cannot detect that a contact address stopped being monitored: schedule your own review.
- Email address limit: 254 characters in total; the console also caps the local part at 64.

## Verify
- [ ] `compute` for SECURITY on a random project returns the security group.
- [ ] Every category you care about has at least one org-level contact.
- [ ] Creating a contact with `@gmail.com` fails under the domain constraint.

## Checked
2026-10-31. Confirmed against the Essential Contacts overview page, the `gcloud essential-contacts create`
reference, the Essential Contacts API v1 discovery document (category enum) and the organization policy
constraints reference. Removed: enabling `essentialcontacts.googleapis.com`, the
`roles/essentialcontacts.admin` requirement, claims that legal/suspension notices cannot be suppressed
and that Owners are the fallback, and the "verification-free notice" claim.
Method: documentation only; no commands were run.

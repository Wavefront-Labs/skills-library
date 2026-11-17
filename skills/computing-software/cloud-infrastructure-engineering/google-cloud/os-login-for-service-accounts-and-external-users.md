---
id: computing-software.cloud-infrastructure-engineering.google-cloud.os-login-for-service-accounts-and-external-users
name: os-login-for-service-accounts-and-external-users
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, os-login, os-login-service-accounts, os-login-external-users, oslogin-external-user, posix-accounts, ansible]
level: advanced
status: docs-checked
description: "Let automation service accounts and users from outside your organisation SSH through OS Login: roles, osLoginExternalUser, key TTLs and registering keys."
sources: ["https://cloud.google.com/compute/docs/oslogin/set-up-oslogin", "https://cloud.google.com/compute/docs/oslogin/manage-oslogin-in-an-org", "https://cloud.google.com/compute/docs/tutorials/service-account-ssh", "https://cloud.google.com/sdk/gcloud/reference/compute/os-login/ssh-keys/add"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OS Login for service accounts and external users

## 1. Service accounts (Ansible, CI, config management)
```bash
SA=ansible@<P>.iam.gserviceaccount.com
gcloud projects add-iam-policy-binding <P> --member=serviceAccount:$SA --role=roles/compute.osAdminLogin
# if target VMs run as a service account, the caller also needs actAs on it
gcloud iam service-accounts add-iam-policy-binding <VM_SA> --member=serviceAccount:$SA --role=roles/iam.serviceAccountUser
# register a key for the SA (as the SA, via impersonation)
gcloud compute os-login ssh-keys add --key-file=ansible.pub --ttl=<TTL> --impersonate-service-account=$SA
gcloud compute os-login describe-profile --impersonate-service-account=$SA --format='value(posixAccounts[0].username)'
```
Use the username that `describe-profile` returns as the SSH user (for example in an Ansible inventory).

## 2. Users outside your organisation
A user from another Cloud Identity/Workspace org (contractor, vendor) needs, **in addition**
to `compute.osLogin`/`osAdminLogin` on the project:
```bash
gcloud organizations add-iam-policy-binding <ORG_ID> \
  --member=user:alice@vendor.com --role=roles/compute.osLoginExternalUser
```
The role is granted on the organization and must be granted by an organization administrator. It lets external Google Accounts configure POSIX account information; also grant the other OS Login instance access roles at the project or organization level. A Google Workspace admin can restrict or permit VM access for users outside the organization.

## 3. Hygiene
- Set a TTL on `ssh-keys add` (`--ttl`) so registered keys expire.
- OS Login 2FA needs `enable-oslogin` and `enable-oslogin-2fa` both set to `TRUE` in instance or project metadata, and users need 2-Step Verification configured.

## Gotchas
- Read the username from the login profile rather than guessing it.
- Stale keys accumulate; list and remove old registered keys.
- With workforce identity federation (Preview in the docs), OS Login uses certificate-based authentication instead of key-based authentication; test before relying on it.

## Verify
- [ ] The service account can SSH using its OS Login username with no metadata keys present.
- [ ] External user can SSH with the roles above.

## Checked
2026-10-31. Confirmed against the OS Login setup page (role table: osLogin, osAdminLogin, serviceAccountUser, osLoginExternalUser on the organization, admin-granted; 2FA metadata keys), the OS Login in an organization page (external users, Workspace controls, workforce identity federation) and the gcloud `os-login ssh-keys add` reference (`--key-file`, `--ttl`). Removed unconfirmed claims: POSIX username formats, the 32 KB profile limit, Ansible and IAP inventory detail, the 2FA-versus-service-account statement, domain restricted sharing behaviour, and the fixed TTL values.
Method: documentation only; no commands were run.

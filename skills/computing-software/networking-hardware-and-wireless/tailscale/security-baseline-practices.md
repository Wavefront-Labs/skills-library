---
id: computing-software.networking-hardware-and-wireless.tailscale.security-baseline-practices
name: security-baseline-practices
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [security-best-practices, mfa, least-privilege]
level: practitioner
status: docs-checked
description: "Follow the docs' baseline steps for client upgrades, contacts, MFA, groups and tags."
sources: ["https://tailscale.com/kb/1196"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Security baseline

Goal: apply the docs' baseline list for a tailnet.

- **Upgrade clients promptly.** Check for updates to see the installed client version on every device, and use auto-updates to keep clients current.
- **Subscribe to security bulletins** (RSS). Tailscale publishes them to disclose security issues.
- **Set a security contact email.** If none is set, security emails go to the tailnet owner email address. Prefer an email group such as `security@example.com` over a personal address. With GitHub as the identity provider, Tailscale has no contact email unless you add one in contact preferences.
- **Enable MFA in your identity provider**, ideally with a hardware token; Tailscale relies on your IdP to authenticate users.
- **Define access control policies** by job function using least privilege (see the grant examples).
- **Use groups** so a role change means editing group membership, not rewriting rules. Enable user and group provisioning to sync groups from your IdP.
- **Use tags** so access follows device purpose rather than owner, so a departing user does not take device access with them.

Related advanced practices from the same page: manage the policy file with GitOps for versioning and an audit trail, and deploy Tailscale with infrastructure as code (Terraform or Pulumi providers).

**Checklist**

1. Auto-updates on.
2. Security contact set to a group address.
3. MFA at the IdP.
4. Groups and tags in all rules.

## Checked

2026-11-09. Confirmed against the Tailscale security best practices page (baseline and advanced practices). Corrected the security contact default and the client version wording, and replaced an unsourced deployment checklist reference with the page's own GitOps and infrastructure as code advice.

Method: docs-checked 2026-11-09 against tailscale.com/kb/1196 (Best practices to secure your tailnet), read in full.

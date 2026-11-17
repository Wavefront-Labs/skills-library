---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-scim-user-provisioning
name: grafana-scim-user-provisioning
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [scim-provisioning, grafana-auth, team-sync-config, grafana-rbac, okta, entra-id]
level: practitioner
status: docs-checked
description: "Provision Grafana users and teams from Entra ID or Okta with SCIM: SAML-only requirement, userUID and externalId alignment, settings, and SCIM vs team sync."
sources: ["https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-scim-provisioning/", "https://grafana.com/docs/grafana/latest/setup-grafana/configure-security/configure-team-sync/", "https://datatracker.ietf.org/doc/html/rfc7644"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SCIM user provisioning

SCIM is an open standard (RFC 7644 defines the protocol) that lets your identity provider automate provisioning of
users and groups to Grafana. Available in Grafana Enterprise and Grafana Cloud. Supported IdPs: Entra ID and Okta.

## Requirements
- SCIM provisioning only works with SAML authentication; other methods are not supported.
- Use the same identity provider for provisioning and for the authentication flow.
- The SAML assertion must include the `userUID` attribute carrying the user's unique identifier at the IdP (Grafana has
  guides for Entra ID and Okta).
- Align the SCIM `externalId` with the SAML identifier: use a stable IdP attribute (for example Entra ID `user.objectid`)
  as the SCIM `externalId`, send the same value as a SAML claim, and set `assertion_attribute_external_uid` in
  `[auth.saml]` to that claim name. If they differ Grafana may not link the user to the SCIM profile, giving incorrect
  access. By default Grafana uses the `userUID` attribute for SCIM linking.

## Grafana settings
UI: Administration > Authentication > SCIM (changes there override config file and environment variables, need no
restart, and work on Grafana Cloud). The UI shows the stack domain, stack ID and tenant URL to use in the IdP.
```ini
[auth.scim]
user_sync_enabled = true            # required to enable user provisioning; default false
group_sync_enabled = false          # create, update, delete teams from IdP groups; default false
reject_non_provisioned_users = false  # block non-SCIM users signing in; Cloud Portal users always can; default false
```
Terraform: `grafana_scim_config` with the same three options.

## SCIM vs team sync
| | Team sync | SCIM |
|---|---|---|
| Users | not provisioned | created, updated and disabled from the IdP |
| Teams | syncs memberships of existing teams, at login (LDAP can sync in the background) | creates, updates and deletes teams from IdP groups |
| Roles | not covered | basic roles via Role Sync, handled separately |

- SCIM group sync and Team Sync cannot be enabled together. SCIM user sync can run alongside Team Sync.
- Team sync providers include Auth Proxy, Entra ID, Generic OAuth, GitHub, GitLab, Google, LDAP, Okta and SAML.

## Verify
- [ ] A user provisioned from the IdP can log in via SAML and is linked to the SCIM profile (matching
  `externalId` and external UID).
- [ ] Only one of SCIM group sync or Team Sync is enabled.
- Troubleshooting steps are in the Grafana "Troubleshoot SCIM provisioning" page, which was not checked here.

## Checked
Checked 2026-11-08 against the Grafana "Configure SCIM provisioning" and "Configure Team Sync" pages. The RFC 7644
source was fetched but only used for the protocol name. Removed: the "recent versions (12.x) and feature toggle"
availability note, the numbered setup outline with service account token and attribute mappings, the deprovisioning
timing claim, the duplicate-user gotcha and token rotation advice, none of which the pages state.
Method: documentation only; no commands were run.

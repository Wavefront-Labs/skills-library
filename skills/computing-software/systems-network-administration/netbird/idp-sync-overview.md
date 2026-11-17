---
id: computing-software.systems-network-administration.netbird.idp-sync-overview
name: idp-sync-overview
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, idp-sync, scim, user-provisioning, synced-groups]
level: practitioner
status: docs-checked
description: "NetBird IdP-Sync overview: automatic user and group provisioning, plan availability, supported providers, generic SCIM and sign-in domain preparation."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/team/idp-sync/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
IdP-Sync provisions users and groups from your identity provider, so joiners get access and leavers lose it without manual steps. Synced groups can be used in access policies and DNS distribution groups.

Availability: NetBird Cloud Team plan and above; self-hosted needs an Enterprise Commercial License; not in Community Edition.

Providers (each with its own guide): Microsoft Entra ID (Graph API or SCIM), Okta, Google Workspace, JumpCloud, Keycloak, IIJ ID (SCIM). Any SCIM-capable IdP can use the Generic SCIM option in the dashboard; for unlisted providers contact support@netbird.io.

Before rollout on Cloud: add every domain your users sign in with as a sign-in domain, or IdP sync cannot add users who already belong to another NetBird account. If a user still fails, see the troubleshooting guide for "User already belongs to another NetBird account".

## Checked

2026-11-04. Confirmed against the NetBird IdP-Sync overview page: automatic user and group provisioning, use in policies and DNS, plan availability, provider list, Generic SCIM, support contact, sign-in domain preparation. Removed the restrictions line (synced groups cannot be renamed or deleted, roles managed in NetBird), which this page does not state.
Method: documentation only; no commands were run.

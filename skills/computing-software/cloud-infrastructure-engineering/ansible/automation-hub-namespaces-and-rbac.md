---
id: computing-software.cloud-infrastructure-engineering.ansible.automation-hub-namespaces-and-rbac
name: automation-hub-namespaces-and-rbac
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, automation-hub, hub-namespaces, hub-rbac, galaxy-ng, collection-namespace, content-approval, ci-service-account, infra-ah-configuration]
level: advanced
status: docs-checked
description: "Design namespaces, groups and roles in private automation hub so teams publish only to their own namespace, curators approve, CI uploads with scoped tokens, and it is all code."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/managing_automation_content/", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/access_management_and_authentication/", "https://github.com/redhat-cop/infra.aap_configuration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automation hub namespaces and RBAC

Goal: each team owns a namespace (`netops`, `platform`), can upload only there, uploads go through
curator approval, and the whole permission model is reproducible from git.

## Model
- **Namespace** = first part of the collection name; must exist before the first upload. Namespace "owners" (groups) can upload, edit metadata, delete versions.
- **Groups** hold users (local or mapped from LDAP/SSO); permissions are granted to groups, never users.
- **Roles** (galaxy_ng RBAC): namespace owners (scoped to a namespace: upload, edit metadata,
  delete versions), collection curators (approve/reject staging uploads), content administrators
  and container-repository owners for EE images. In AAP 2.5 the platform gateway's unified access
  UI assigns these; check the hub API for the exact role identifiers.

## Typical design
| Group | Role | Scope |
|---|---|---|
| `hub-netops-publishers` | namespace owner | `netops` |
| `hub-platform-publishers` | namespace owner | `platform` |
| `hub-curators` | collection curator | global |
| `hub-ci-netops` (service user) | namespace owner | `netops` only |
| `hub-readers` / all users | none needed | published content is readable by any authenticated user |

## As code
The `infra.aap_configuration` collection automates hub groups, namespaces and role grants
(roles `hub_group`, `hub_namespace`, `hub_group_roles`, `hub_user`; they drive the certified
`ansible.hub` modules). Connect with the hub host plus an admin token, and keep the group/namespace
definitions in git. See the collection's docs for the variable format.

## CI uploads
Create a service user in `hub-ci-netops`, log in once, create its API token, store it in CI
secrets. `ansible-galaxy collection publish netops-routing-1.3.0.tar.gz --server hub_staging`
lands in staging; a curator approves (or automate approval only for signed builds from protected branches).

## Gotchas
- Treat CI tokens as long-lived credentials: rotating one breaks every pipeline using it (the
  hub's installer token variable notes that a regenerated token invalidates the old).
- The namespace in `galaxy.yml` must match exactly; uploads to an unowned namespace fail with 403.
- Deleting a namespace requires deleting its collections first; prefer deprecating.
- SSO-mapped group membership is evaluated at login; removing someone from the IdP group takes effect on their next login, tokens keep working until revoked.

## Verify
- [ ] A netops CI token can publish `netops.*` and gets 403 publishing `platform.*`.
- [ ] A non-curator cannot approve; the upload waits in staging until a curator approves.

## Checked

- 2026-10-31: namespaces and approval pipelines in private automation hub, approval/signing
  configuration (`automationhub_require_content_approval`, signing services), offline/API tokens,
  group-based access via the gateway, `ansible-galaxy collection publish` and the `infra.aap_configuration`
  hub role names (`hub_group`, `hub_namespace`, `hub_group_roles`, `hub_user`) confirmed in AAP 2.5
  Managing automation content, the RPM installation guide, and the redhat-cop roles listing.
- Removed: the `galaxy.*` role-identifier enums (galaxy-ng docs serve only a landing page; replaced
  with functional role descriptions), the `infra.ah_configuration.ah_*` module names (superseded by
  the `hub_*` roles) and the custom `module_defaults` connection block.
Method: documentation only; no commands were run.

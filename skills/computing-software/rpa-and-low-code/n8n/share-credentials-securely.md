---
id: computing-software.rpa-and-low-code.n8n.share-credentials-securely
name: share-credentials-securely
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, credentials, sharing, projects, can-use, permissions]
level: practitioner
status: docs-checked
description: "Share n8n credentials with users or projects so they can run workflows without seeing secrets: who may share, the Sharing tab, Can use role and removing access."
sources:
  - https://docs.n8n.io/administer/manage-credentials/share-credentials-securely
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let others run or publish workflows with a credential without exposing its details. Availability: n8n Cloud all plans; self-hosted Business and Enterprise.

## Who can share
- Users share credentials they created and own.
- Only project admins share credentials owned by a project.
- Instance owners and admins can view and share all credentials.
- On the **Sharing** tab only the owner or users with share permission can change recipients.
- Members of a team project need not share their own credentials to use them there; share when other people must run or publish workflows with it.

## Steps
1. Left menu: **Overview** or a project, then **Credentials**.
2. Open the credential, select **Sharing**.
3. In **Share with projects or users** pick users or projects.
4. **Save**. Recipients get **Can use**: run and publish, but not view or edit details.
To unshare: same path, remove the recipient, **Save**.

## Sharing tab
- Shared projects: members use it per their project role.
- Projects using it without a share: a member put their personal credential in a project workflow; the project shows **Can view**, so members see it on the workflow but cannot use or edit it. Select **Share** to give the whole project access.
- In team projects, Owners and Admins follow the same rules: they use your credential only after you share it; their instance role extends only to their personal space.
- Sharing an end-user credential shares the credential, not a connection; recipients connect their own account.

## Checked
Method: docs-checked 2026-11-09 against the n8n "Share credentials securely" page (docs.n8n.io, read in full).
Nothing removed; availability, sharing rules, steps and Sharing tab behaviour match the page.

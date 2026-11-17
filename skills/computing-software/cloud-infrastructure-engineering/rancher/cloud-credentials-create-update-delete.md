---
id: computing-software.cloud-infrastructure-engineering.rancher.cloud-credentials-create-update-delete
name: cloud-credentials-create-update-delete
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [cloud-credentials, node-drivers, authentication, infrastructure-provider, ownership]
level: intro
status: docs-checked
description: "Create, update and delete Rancher cloud credentials: types follow active node drivers, credentials belong to their creator, admins see all."
sources:
  - https://ranchermanager.docs.rancher.com/reference-guides/user-settings/manage-cloud-credentials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cloud credentials are the stored authentication values Rancher uses to talk to an infrastructure provider when provisioning clusters. Creating or associating one is normally part of cluster creation; this page covers managing them directly.

The key ownership rule: credentials are **bound to their creator's user profile and cannot be shared between non-admin users**. Administrators can view and manage the credentials of other users.

Create: **Cluster Management > Cloud Credentials > Create**, pick a type (the list is based on the **active** node drivers), give it a name and enter the provider-specific values.

Update: choose the credential, **Edit Config**, change the values and **Save**. The page presents this as the way to rotate changed or compromised access credentials while keeping the same node template.

Delete: use the menu on one credential, or select several and click **Delete** for bulk removal, then confirm.

The credential type dropdown is based on the active node drivers in Rancher.

## Checked

2026-11-09. Read in full the Rancher Manager Managing Cloud Credentials page (reference-guides/user-settings/manage-cloud-credentials). Removed the GKE sentence and two inferences the page does not state.

Method: documentation only; no commands were run.

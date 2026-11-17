---
id: computing-software.cybersecurity-defensive.zitadel.actions-v1-role-on-external-registration
name: actions-v1-role-on-external-registration
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, actions, external-authentication, post-creation, roles, flows]
level: advanced
status: docs-checked
description: "Assign a role automatically when a user registers through an external identity provider using a v1 action in the external authentication flow."
sources:
  - https://zitadel.com/docs/guides/manage/customize/behavior
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
This v1 action grants a role to users who register through an external provider.

Prerequisites: you are at least an ORG_OWNER, your organization has the actions feature enabled, at least one external identity provider is enabled, and a project has at least one role.

Steps:

1. Select Projects, open a project with a role and copy the Project ID at the top right. Note a role key in the ROLES section.
2. Select Actions, then New in the Actions section. Name the action `addGrant`, paste the snippet shown in the guide (a function that pushes a user grant with a project ID and role keys), replace the placeholders and Save.
3. In the Flows section choose New. Set the Flow Type to External Authentication and the Trigger Type to Post Creation.
4. In the Actions dropdown check `addGrant` and Save.

New users who register by authenticating with an external provider now receive the role automatically.

The snippet uses the project ID and role key from step 1, so mismatched placeholders are the first thing to check if no role appears. Compare with the newer Actions v2, which run in addition to these actions and are the extension path described in the concepts page.

## Checked
2026-11-08. Confirmed against the ZITADEL Behavior Customization guide: prerequisites, steps in Projects, Actions and Flows, flow type External Authentication with trigger Post Creation, action name addGrant. Removed: the reference to a repository script path, since the guide inlines the snippet.
Method: documentation only; no commands were run.

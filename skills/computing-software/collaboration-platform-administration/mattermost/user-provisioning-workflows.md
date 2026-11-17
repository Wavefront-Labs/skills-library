---
id: computing-software.collaboration-platform-administration.mattermost.user-provisioning-workflows
name: user-provisioning-workflows
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [user-provisioning, deprovisioning, id-attribute, deactivate-user]
level: practitioner
status: docs-checked
description: "Choose a Mattermost provisioning route (on demand, bulk import, API), pick a stable user identifier and deprovision users correctly."
sources: ["https://docs.mattermost.com/administration-guide/onboard/user-provisioning-workflows.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# User provisioning and deprovisioning

Three recommended ways to create users:
1. On demand: with no pre-provisioning, an account is created at first login, and the user is asked to pick a team to join.
2. Pre-provisioned by bulk import: the bulk loading tool adds users to teams and channels before they first log in.
3. Mattermost REST API: create accounts and add or remove them from teams and channels programmatically, as enterprises commonly do from identity workflows.

User identifier depends on authentication: email/password uses the email address or username; AD/LDAP needs a unique, unchanging ID Attribute configured, because if it changes Mattermost creates a new account unrelated to the old one; SAML 2.0 binds on a selected attribute, and an ID that is unique and stable is preferred over email. As long as the ID attribute is unique and stable, email, name and other attributes can change without breaking the account.

Deprovisioning (deactivation) options: AD/LDAP synchronisation reflecting directory status; System Console > Users for email/password accounts; the REST API user delete operation; and mmctl user deactivate. Deactivated users remain in the database and their messages stay visible. Permanent removal is done with mmctl user delete. From v10.10, deactivating an account automatically sets its availability to offline.

Plan: decide the identifier first, pick the provisioning route that matches your identity source, and wire deprovisioning to the same source so leavers are deactivated without manual steps.

## Checked

Confirmed against the Provisioning workflows page: the three provisioning routes, user identifier rules per authentication method, the four deactivation routes, retention of deactivated users, mmctl user delete and the v10.10 offline availability change. The closing plan is the author's advice.

Method: docs-checked 2026-11-09 against the full administration-guide/onboard/user-provisioning-workflows page (source rst from the mattermost/docs repo).

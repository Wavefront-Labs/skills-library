---
id: computing-software.cybersecurity-defensive.dex.dex-microsoft-connector-groups
name: dex-microsoft-connector-groups
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [microsoft, groups, admin-consent, whitelist]
level: advanced
status: docs-checked
description: "Return and restrict Microsoft groups in Dex: Directory.Read.All consent, onlySecurityGroups, groupNameFormat, groups list and useGroupsAsWhitelist."
sources:
  - https://dexidp.io/docs/connectors/microsoft/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Group support needs the `groups` scope plus an explicit organisation administrator consent so Dex can list groups on behalf of the logged in user.

Consent steps:

1. When registering the Dex app, add the `Directory.Read.All` permission to the Delegated Permissions.
2. Open this link as an organisation admin: `https://login.microsoftonline.com/<tenant>/adminconsent?client_id=<dex client id>`.
3. Set `tenant` to a tenant uuid or tenant name; group lookup does not work with the generic values.

Options:

```yaml
config:
  tenant: myorg.onmicrosoft.com
  onlySecurityGroups: true
  groupNameFormat: id
  groups:
  - developers
  - devops
  useGroupsAsWhitelist: true
```

- `onlySecurityGroups`: restrict to security groups. By default all groups (security, Office 365, mailing lists) are included.
- `groupNameFormat: id`: keep group ids. By default Dex resolves ids to names.
- `groups`: require membership in at least one listed group to log in.
- `useGroupsAsWhitelist`: restrict the groups claim to only the user's groups that are in the configured list.

Gotcha: with a group requirement set, users outside those groups fail authentication even if their Microsoft login is valid.

## Checked

2026-11-03: read against Dex docs, Microsoft connector (https://dexidp.io/docs/connectors/microsoft/).

Removed or corrected: Nothing removed.

Method: documentation only; no commands were run.

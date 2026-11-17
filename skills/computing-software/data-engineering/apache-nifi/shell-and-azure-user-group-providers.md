---
id: computing-software.data-engineering.apache-nifi.shell-and-azure-user-group-providers
name: shell-and-azure-user-group-providers
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, shellusergroupprovider, azuregraphusergroupprovider, authorizers, groups]
level: advanced
status: docs-checked
description: "ShellUserGroupProvider and AzureGraphUserGroupProvider settings in authorizers.xml: refresh delays, exclusions, Graph endpoints, group filters, page size and username claim."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Shell and Azure group providers

Both ship commented out in `authorizers.xml`.

ShellUserGroupProvider:
- `Initial Refresh Delay`: 5 mins
- `Refresh Delay`: 5 mins
- `Exclude Groups`, `Exclude Users`: regular expressions; default `''`, which excludes nothing
- Runs shell commands such as getent on Linux and dscl on macOS

AzureGraphUserGroupProvider:
- `Refresh Delay`: 5 mins
- `Authority Endpoint` (example `https://login.microsoftonline.com`)
- `Graph Endpoint`: `https://graph.microsoft.com/v1.0`
- `Graph Scope`: `https://graph.microsoft.com/.default`
- `Directory ID`, `Application ID`, `Client Secret` (no defaults; keep the secret as a placeholder in notes)
- Filters matched against the group displayName: `Group Filter Prefix`, `Suffix`, `Substring`, `List Inclusion`; at least one filter condition should be specified, and List Inclusion avoids fetching every group when no string filter is set
- Needs an Azure app registration with Microsoft Graph Group.Read.All and User.Read.All permissions (admin consent), a client secret, and ID token claims for upn and/or email
- `Page Size`: 50 (max 999; 0 disables paging)
- `Claim for Username`: `upn`

Verify: after the refresh delay, the expected users and groups appear on the NiFi Users page.

## Checked

Confirmed in the NiFi Administration Guide, ShellUserGroupProvider and AzureGraphUserGroupProvider sections: refresh delays of 5 mins, exclude defaults, endpoint and scope defaults, page size default 50 and max 999 with 0 disabling paging, Claim for Username default upn, filter names, app registration requirements, and the commented-out default. Nothing was removed.

Method: docs-only read of cited pages, 2026-11-08

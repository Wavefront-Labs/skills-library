---
id: computing-software.database-administration.influxdb.organization-members-and-owners
name: organization-members-and-owners
category: computing-software
field: database-administration
product: influxdb
tags: [organizations, influx-org-members, owner, membership, rbac]
level: practitioner
status: docs-checked
description: "Add users to an organization, optionally as owner, with influx org members add using the org name and user ID."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/organizations/members/add-member/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

```sh
influx user list                      # find the user ID

influx org members add -n <org-name> -m <user-ID>

# make the user an owner
influx org members add -n <org-name> -m <user-ID> --owner
```

`--owner` adds the user as an owner across all organizations and requires an operator token.

To detach a user from an organization use `influx org members remove`; to delete the user entirely use `influx user delete`. See each command's reference for flags.

## Checked

Method: docs-checked 2026-11-09 against the InfluxDB v2 "Add a member to an organization" page, article body (lines 574-594) read from the downloaded text. The remove and delete command names were confirmed only from the page's CLI navigation list.

Removed: the paragraph on membership versus token permissions and scoped tokens for service accounts, which the page does not state.

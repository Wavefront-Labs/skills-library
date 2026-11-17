---
id: computing-software.database-administration.influxdb.create-users-and-set-passwords
name: create-users-and-set-passwords
category: computing-software
field: database-administration
product: influxdb
tags: [users, influx-user-create, influx-user-password, operator-token]
level: practitioner
status: docs-checked
description: "Create, change the password of and delete OSS users with the influx CLI and an operator token; none of these can be done in the UI."
sources:
  - https://docs.influxdata.com/influxdb/v2/admin/users/create-user/
  - https://docs.influxdata.com/influxdb/v2/admin/users/change-password/
  - https://docs.influxdata.com/influxdb/v2/admin/users/delete-user/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

User management is CLI-only and needs an operator token (via config, `INFLUX_TOKEN` or `-t`).

```sh
influx user create --org ORG_NAME --name USER_NAME --password USER_PASSWORD
influx user list
influx user password --name USERNAME --password PASSWORD
influx user delete --id USER_ID
```

- If `--password` (`-p`) is omitted on `user create`, the new user is prompted for one.
- `user password` takes the username (`--name`) or ID (`--id`); without `--password` you are prompted.
- `user delete` needs the user ID from `influx user list` and removes the user completely. To remove a user from an organization without deleting the user, remove them as a member of the organization instead.

Tokens stop working when the user who created them is deleted.

## Checked

- Date: 2026-11-04
- Confirmed against: https://docs.influxdata.com/influxdb/v2/admin/users/create-user/, https://docs.influxdata.com/influxdb/v2/admin/users/change-password/, https://docs.influxdata.com/influxdb/v2/admin/users/delete-user/
- Scope: user create, password and delete commands and the operator-token requirement.
- Removed: the `influx org members remove` command name and the shell-history advice.
Method: documentation only; no commands were run.

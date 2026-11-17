---
id: computing-software.web-development.strapi.admin-user-commands
name: admin-user-commands
category: computing-software
field: web-development
product: strapi
tags: [strapi, admin-create-user, reset-password, administrator, cli]
level: practitioner
status: docs-checked
description: "Manage Strapi administrator accounts from the CLI: admin:create-user, reset-user-password, list-users, active-user, block-user and delete-user with their options."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Administration commands

The CLI page lists six commands: `admin:create-user`, `admin:reset-user-password`, `admin:list-users`, `admin:active-user`, `admin:block-user`, `admin:delete-user`. Each has a shorter alias, shown in the table.

Interactive commands such as `strapi admin:create-user` don't display prompts with `npm`; the docs suggest `yarn`.

| Command | Alias | Options |
|---|---|---|
| `admin:create-user` | `admin:create` | `-f --firstname` (required), `-l --lastname`, `-e --email` (required), `-p --password` |
| `admin:reset-user-password` | `admin:reset-password` | `-e --email`, `-p --password` |
| `admin:list-users` | `admin:list` | none; prints a table with ID, email, names, active status, blocked status and roles |
| `admin:active-user` | `admin:active` | `-e --email` (required), `-a --active` (`true` or `false`, required) |
| `admin:block-user` | `admin:block` | `-e --email` (required), `-b --block` (`true` or `false`, required) |
| `admin:delete-user` | `admin:delete` | `-e --email` (required) |

Where options are omitted for create, reset, active, block and delete, the command prompts for them interactively.

```bash
strapi admin:create-user --firstname=Kai --lastname=Doe --email=chef@strapi.io --password=Gourmet1234
strapi admin:reset-user-password --email=chef@strapi.io --password=Gourmet1234
strapi admin:active-user --email=chef@strapi.io --active=true
strapi admin:block-user --email=chef@strapi.io --block=true
strapi admin:delete-user --email=chef@strapi.io
```

Delete caution: the confirmation prompt appears only in interactive mode. Passing `--email` deletes the account without confirmation.

Admin accounts are separate from end users managed by Users & Permissions.

## Checked
Confirmed 2026-11-08 against the Administration section of the Strapi CLI reference (lines for admin commands read in full; the rest of that long page was not read). The earlier draft listed only create and reset; added the option tables, the four other commands, and the no-confirmation delete behaviour. The draft's reset example without options is replaced by the docs' form with options.
Method: docs-only read of cited pages, 2026-11-08

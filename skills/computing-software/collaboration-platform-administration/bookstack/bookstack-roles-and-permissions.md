---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-roles-and-permissions
name: bookstack-roles-and-permissions
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, roles, permissions, entity-permissions, inheritance, everyone-else, shelves, access-control]
level: practitioner
status: docs-checked
description: "Model BookStack access: system roles versus content permissions, own versus all, inheritance from book and chapter, non-cascading shelves, Everyone Else and precedence rules."
sources: ["https://www.bookstackapp.com/docs/user/roles-and-permissions/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack roles and permissions

Three layers: system permissions on a role (system-wide abilities), asset permissions on a role (default abilities on content), and content-level permissions on shelves, books, chapters and pages, which need a role with "Manage all/own permissions".

A user can hold several roles and gets an ability if any role grants it. Many asset permissions have an "Own" option limited to items the user owns. The admin role keeps all permissions.

Inheritance: custom permissions on a book or chapter cascade to children unless a child has its own. Shelves are the exception: they do not cascade, because shelf-to-book is many-to-many, but their permissions can be copied to all child books in one action (`bookstack:copy-shelf-permissions` in the CLI).

"Everyone Else" controls roles with no specific entry on the item. It defaults to "Inherit defaults"; unchecking it applies the permissions in its row.

Precedence, least to most specific: role permissions, "Everyone Else" content permissions, role-specific content permissions. A more specific rule wins and can deny a less specific one; an inherited role-specific permission behaves as if set on the item unless a lower level sets its own for that role. If a grant and deny conflict at the same specificity, the grant wins.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) user/roles-and-permissions/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: nothing.
Method: documentation only; no commands were run.

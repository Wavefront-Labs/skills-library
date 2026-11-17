---
id: computing-software.collaboration-platform-administration.bookstack.bookstack-artisan-commands
name: bookstack-artisan-commands
category: computing-software
field: collaboration-platform-administration
product: bookstack
tags: [bookstack, artisan, create-admin, reset-mfa, update-url, clear-revisions, cleanup-images, regenerate-search, copy-shelf-permissions]
level: practitioner
status: docs-checked
description: "Use BookStack artisan commands: create-admin and reset-mfa for lockouts, update-url, copy-shelf-permissions, clearing activity and revisions, image cleanup and index regeneration."
sources: ["https://www.bookstackapp.com/docs/admin/commands/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# BookStack artisan commands

Run from the install folder as `php artisan <command>`; add `-h` for options.

- `bookstack:create-admin`: interactive, or `--email`, `--name`, `--password`, `--generate-password`, `--external-auth-id` (LDAP/SAML2/OIDC). `--initial` updates `admin@admin.com` if present, else creates an admin if none exists, else exits with code 2.
- `bookstack:reset-mfa --email=<email>` or `--id=<id>`: clears a user's MFA; they re-enrol if their role enforces it.
- `bookstack:update-url <oldUrl> <newUrl>`: find and replace a base URL in the database. Back up first; it does not change `APP_URL`.
- `bookstack:copy-shelf-permissions --all` or `--slug=<shelf>`: shelf permissions do not cascade, this copies them to child books.
- `bookstack:cleanup-images`: removes images unused in page content (CLI avoids timeouts).
- `bookstack:clear-revisions` (`-a` also drops update drafts), `bookstack:clear-activity` (audit log and recent activity), `bookstack:clear-views`.
- `bookstack:regenerate-search`, `bookstack:regenerate-permissions`, `bookstack:regenerate-references`: rebuild indexes; rarely needed manually.
- `bookstack:assign-sort-rule <rule_id> --all-books | --books-without-sort | --books-with-sort=<id>`; with no args lists rules.
- `bookstack:refresh-avatar` (`--email`, `--id`, `--users-without-avatars`, `--all`; Gravatar only).
- `bookstack:install-module <location>`: install a theme module from a path or URL.
- `bookstack:delete-users`: deletes all users except the original admin and system users.
- `bookstack:db-utf8mb4`: generates SQL to upgrade the database to utf8mb4 for emoji.

## Checked

2026-11-03. Confirmed against the BookStack docs page(s) admin/commands/ (under https://www.bookstackapp.com/docs/), including the prose, not only identifiers.
Removed or reworded: nothing.
Method: documentation only; no commands were run.

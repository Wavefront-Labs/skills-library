---
id: computing-software.systems-network-administration.audiobookshelf.reset-root-password
name: reset-root-password
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [password-reset, root, sqlite, users-table, dbeaver]
level: sme
status: docs-checked
description: "Reset a user password in Audiobookshelf from the admin page, or clear the root password by setting pash to NULL in the SQLite users table."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/faq/server.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/install/11.env-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For a normal account, an admin resets the password on the **User** page of the server settings. If the user logs in through OIDC, reset the password in the OIDC provider instead.

For a forgotten **root** password you must edit the SQLite database manually. DBeaver is suggested for people unfamiliar with SQLite editing.

1. Stop the server. Make sure it is not running while editing and close the database before starting it again.
2. Open the database and the `users` table.
3. Find the root user row and update the `pash` column to NULL.
4. Start the server and log in as root with a blank password.
5. Set a new password immediately after logging in.

There is no default username or password; the root credentials are created on first visit to the web UI.

Take a backup of the database file before editing it. For the database location see the `CONFIG_PATH` setting, which in Docker is the `/config` mount.

## Checked

Method: docs-checked 2026-11-09 against the FAQ server page, the environment configuration page (CONFIG_PATH) and the Docker install page (/config mount), all full raw markdown from the Audiobookshelf docs repo.

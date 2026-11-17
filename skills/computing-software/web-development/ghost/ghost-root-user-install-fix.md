---
id: computing-software.web-development.ghost.ghost-root-user-install-fix
name: ghost-root-user-install-fix
category: computing-software
field: web-development
product: ghost
tags: [ghost, ghost-cli, root-user, permissions, digitalocean, migration]
level: intro
status: docs-checked
description: "Migrate a Ghost install from root to a regular Linux user after Ghost-CLI refuses to run as root."
sources:
  - https://github.com/TryGhost/docs/blob/main/faq/root-user-fix.mdx
  - https://github.com/TryGhost/docs/blob/main/install/ubuntu.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: fix the error that appears on DigitalOcean one-click installs set up as root.

Since Ghost-CLI 1.5.0, running Ghost commands as root is disallowed. The error says to create a user with regular privileges and migrate the install.

Run as root:
1. `adduser <newuser>` and `usermod -aG sudo <newuser>`.
2. Create the instance directory and move config: `mkdir -p /path/to/<newuser>-home/.ghost/`, `chown <newuser>:<newuser> /path/to/<newuser>-home/.ghost`, `mv /path/to/root-home/.ghost/config /path/to/<newuser>-home/.ghost/config`, then chown the moved file.
3. Change into the Ghost install directory (the page says `/var/www/ghost/` is the default in the DigitalOcean One-Click installs) and hand over ownership: `find . -group root -user root -exec chown <newuser>:<newuser> {} \;`. The page says this might take a while.
4. Log in as the new user with `su - <newuser>`, then run `ghost ls` to see whether the installation is still up and running.

Do not name the new user `ghost`; the Ubuntu install guide warns it conflicts with the Ghost-CLI.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 60 lines, no imported snippets): faq/root-user-fix.mdx, and install/ubuntu.mdx (245 lines) for the `ghost` username warning. The page's own home paths are written here as placeholders. Removed: the "remaining steps in the FAQ" wording (the page's last step is the login) and `ghost doctor` from the Verify step (page only names `ghost ls`).
Method: documentation only; no commands were run.

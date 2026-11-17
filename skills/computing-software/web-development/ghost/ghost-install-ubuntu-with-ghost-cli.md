---
id: computing-software.web-development.ghost.ghost-install-ubuntu-with-ghost-cli
name: ghost-install-ubuntu-with-ghost-cli
category: computing-software
field: web-development
product: ghost
tags: [ghost, install, ubuntu, nginx, mysql, ghost-cli, lets-encrypt]
level: practitioner
status: docs-checked
description: "Install Ghost in production on Ubuntu with MySQL, NGINX, systemd and Let's Encrypt SSL using Ghost-CLI."
sources:
  - https://github.com/TryGhost/docs/blob/main/install/ubuntu.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a production Ghost site on a fresh Ubuntu server.

Prerequisites: Ubuntu 22.04, 24.04 or 26.04, NGINX (minimum 1.9.5 for SSL), a supported Node.js version, MySQL 8.0 or 8.4, systemd, at least 1GB memory, and a domain with a DNS A record pointing to the server before you start (needed for SSL).

Server setup: log in as root, create a non-root user (do not name it `ghost`, which conflicts with the CLI), add it to the sudo group, update packages, then install NGINX, MySQL and Node.

Install:
1. `sudo npm install ghost-cli@latest -g`
2. `sudo mkdir -p /var/www/sitename && sudo chown <user>:<user> /var/www/sitename && sudo chmod 775 /var/www/sitename`
3. `cd /var/www/sitename && ghost install`

Answer the prompts: blog URL (with protocol), MySQL host, user and password, database name, create a dedicated ghost MySQL user (recommended), set up NGINX, SSL (Let's Encrypt, asks for an email), systemd, and whether to start Ghost. Then create the owner account at `https://example.com/ghost`.

Recovery: `ghost uninstall` after a failed install, `ghost setup` after an interrupted one.

Note: Ghost-CLI installs do not support web analytics and use the hosted ActivityPub service; the Docker method covers those.

MySQL root: on newer Ubuntu the MySQL root user uses socket-based authentication, which Ghost does not support, so give root a password first (the guide uses `ALTER USER 'root'@'localhost' IDENTIFIED WITH 'caching_sha2_password' BY '<your-new-root-password>'; FLUSH PRIVILEGES;` inside `sudo mysql`). Blog URL must be the exact URL with protocol; IP addresses cause errors. SSL can also be set up later with `ghost setup ssl`. The guide is not suitable for local use or contributing to core.

## Checked

Date: 2026-11-07. Read in full (GitHub blob text, 245 lines, no imported snippets): install/ubuntu.mdx. Versions, prerequisites, commands, prompts and recovery steps match. The guide's Node.js step uses a NodeSource repository with `NODE_MAJOR` left to a supported version; no Node version is claimed here. Removed the Verify line (the page only says to open `/ghost` to create the owner account) and added the MySQL root and `ghost setup ssl` details.
Method: documentation only; no commands were run.

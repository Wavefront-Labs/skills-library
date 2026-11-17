---
id: computing-software.messaging-and-integration.node-red.node-red-admin-cli-and-palette-manager
name: node-red-admin-cli-and-palette-manager
category: computing-software
field: messaging-and-integration
product: node-red
tags: [node-red, node-red-admin, palette-manager, install-nodes, hash-pw, npm, admin-api, remote-administration]
level: practitioner
status: docs-checked
description: "Administer a Node-RED instance remotely with node-red admin: target, login, list, info, search, install, enable, disable, remove and hash-pw."
sources: ["https://nodered.org/docs/user-guide/node-red-admin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# node-red admin command-line tool

Since Node-RED 1.1.0 the admin tool is built into the `node-red` command: use `node-red admin <command>`. If you install the separate package (`npm install -g node-red-admin`) the command is `node-red-admin <command>`; this uses `sudo` for non-root users on Linux and macOS, or an Administrator shell on Windows.

By default it targets `http://localhost:1880`. Point it at another instance with `node-red-admin target http://node-red.example.com/admin`. If authentication is enabled, run `node-red-admin login`. These commands create `~/.node-red/.cli-config.json`, which stores the target and access token. `hash-pw` needs no login.

Commands: `target` (set or view the target URL), `login`, `list` (installed nodes), `info` (module or node details), `enable`, `disable` (module or node set), `search` (modules to install), `install` (from npm), `remove`, and `hash-pw` (creates a password hash for the `adminAuth` and `httpNodeAuth` settings).

## Checked

2026-11-04. Confirmed against the Node-RED user guide page Command-line Administration. Removed: the Palette Manager paragraph and the Docker /data note (not on the cited page), and the bcrypt wording for hash-pw.

Method: documentation only; no commands were run.

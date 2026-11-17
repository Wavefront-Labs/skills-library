---
id: computing-software.collaboration-platform-administration.mattermost.license-key-installation
name: license-key-installation
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [license-key, mmctl-license, edition-and-license, high-availability-license]
level: practitioner
status: docs-checked
description: "Install or replace a Mattermost license in the System Console or with mmctl license upload, with HA, downgrade and storage notes."
sources: ["https://docs.mattermost.com/administration-guide/manage/admin/installing-license-key.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing and changing a license key

Add or change a license either way:
- System Console > About > Edition and License, then upload the license key file; the license details display once it is installed.
- mmctl license upload [license] [flags], which uploads a new license or replaces the existing one; restart the server when it completes. In a high availability environment the new license file must be updated on every node.

Notes:
- From v10.11 the option to add a license in the console is disabled when the license is set using an environment variable.
- Enterprise customers with the Premier Support add-on can request a staging license for testing.
- Removing an Enterprise or Professional license does not delete Enterprise settings, but those features stop working until a license is applied again. Applying Enterprise to a server previously on Professional keeps the Professional settings; applying Professional to a previously Enterprise server keeps Enterprise settings but they become inaccessible.
- In a high availability cluster, every server must have the same Enterprise license installed.

Changing a key: you do not have to wait for expiry. The server checks only the seat count and the end date, not the start date, so a new license can be applied early. Before uploading, review System Console > Reporting > System Statistics: Total Activated Users is the primary paid seat count used for validation, and single-channel guests are shown separately. From v6.7 just upload the new file; on older releases first select Remove Enterprise License and Downgrade Server.

Storage: an uploaded license is kept in the SQL database in the Licenses table; select * from mattermost.Licenses lists the keys on the server.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/manage/admin/installing-license-key. Corrected the environment-variable note and added the high-availability node requirement.

Method: documentation only; no commands were run.

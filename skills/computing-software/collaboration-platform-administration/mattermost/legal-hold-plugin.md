---
id: computing-software.collaboration-platform-administration.mattermost.legal-hold-plugin
name: legal-hold-plugin
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [legal-hold, litigation-hold, compliance, processor-tool]
level: advanced
status: docs-checked
description: "Run a Mattermost Legal Hold with the Legal Hold plugin: install, schedule, create, secret verification, download and process data, release."
sources: ["https://docs.mattermost.com/administration-guide/comply/legal-hold.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Legal Hold workflow

A Legal Hold (litigation hold) preserves relevant information when litigation, a regulatory investigation, an audit or a records-management suspension is anticipated. In Mattermost it is an Enterprise feature delivered by the Legal Hold plugin, and only system admins can operate it. It complements data retention and eDiscovery but is not the same as eDiscovery: a hold preserves the electronically stored information, eDiscovery then identifies, collects, reviews and produces it.

Steps:
1. Define a hold policy with legal counsel, including how relevant users are identified.
2. Install the plugin. From Mattermost v12.0 it is pre-packaged with the server: select App Marketplace in the Product menu, find Legal Hold Plugin and Install. On releases before v12.0 download the plugin binary (compatible with Mattermost v8.0.1 and later) and upload it through System Console > Plugins > Plugin Management > Upload Plugin. Then Enable it under Installed Plugins in Plugin Management. Configure when it runs using the format HH:MM +/-HHMM (+0000 for UTC). Optionally set a custom Amazon S3 bucket; otherwise the server file store is used. If the bucket has versioning enabled, use a dedicated bucket without versioning, because the plugin frequently rewrites files in the legalhold directory and each change creates a new version.
3. Create the hold under System Console > Plugins > Legal Hold Plugin > Create new: name, users or user groups, optional inclusion of public channels (excluded by default; including them greatly increases data), start date and optional end date. Data is only downloadable after the next scheduled job, which can take up to 24 hours.
4. Manage: Edit changes name, users, end date and public channel inclusion. Show reveals the Legal Hold secret for verifying authenticity. Download fetches the preserved zip.
5. Release the hold when done. Release irreversibly deletes the held data.

To read the zip, use the processor tool from the plugin's GitHub releases: ./processor --legal-hold-data ./legalholddata.zip --output-path <dir> --legal-hold-secret "<KEY>" produces a self-contained HTML site, and the optional secret verifies each file (a mismatch reports a hash error).

Coverage: messages and files in public, private, direct and group channels, including plugin, bot and webhook posts, even if users delete them or later leave, and archived channels (until retention purges them). Not covered: reactions, collaborative playbooks and audio calls. Users are not notified.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/comply/legal-hold. Corrected the install step: the plugin is pre-packaged from v12.0 and the v8.0.1 binary upload applies to earlier releases.

Method: documentation only; no commands were run.

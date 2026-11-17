---
id: computing-software.collaboration-platform-administration.mattermost.channel-export-plugin
name: channel-export-plugin
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [channel-export, export-command, csv-export, plugin-marketplace]
level: intro
status: docs-checked
description: "Install and use the Mattermost Channel Export plugin to export a channel's messages to CSV with the export slash command."
sources: ["https://docs.mattermost.com/administration-guide/comply/export-mattermost-channel-data.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Export channel data

The Channel Export integration moves channel data out for analysis, migration or backup. On Mattermost Cloud no setup is needed. On self-hosted servers a system admin installs it from the in-product App Marketplace.

Enable:
1. Product menu > App Marketplace.
2. Find Channel Export and select Install.
3. Select Configure, which opens the System Console page for the plugin.
4. Enable and configure the plugin and Save. Options include restricting channel export to system, team and channel admins only, and configuring a maximum file size for channel export files.

Use: only a system admin can export channel data. In the channel to export, run the /export slash command; the channel's message data is produced as a CSV-formatted file.

Upgrade: update the plugin as new versions are released; updates are generally seamless and do not interrupt users. Releases are listed on the plugin's GitHub page.

Help: Mattermost customers can open a support case; bugs go to the plugin's GitHub repository; community questions go to the Integrations and Apps channel on the Mattermost community server. The plugin has a server part and a web app part, and its README explains how to customise it.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/comply/export-mattermost-channel-data. Corrected the maximum to a file size setting; removed the comparison with bulk export.

Method: documentation only; no commands were run.

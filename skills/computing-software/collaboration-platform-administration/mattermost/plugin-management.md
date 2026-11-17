---
id: computing-software.collaboration-platform-administration.mattermost.plugin-management
name: plugin-management
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [plugins, marketplace, mmctl, plugin-upload]
level: practitioner
status: docs-checked
description: "Install, enable, update and remove Mattermost plugins through the Marketplace, uploads or mmctl, with the settings that gate each method."
sources: ["https://docs.mattermost.com/administration-guide/configure/manage-plugins.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing and managing plugins

Only system admins manage plugins, and they apply to the whole deployment. Gating settings in System Console > Plugins > Plugin Management: Enable plugins (PluginSettings.Enable, default true), Enable Marketplace (EnableMarketplace, default true), Enable remote Marketplace (EnableRemoteMarketplace, default true; set false on servers without internet so only pre-packaged and installed plugins appear), Upload Plugin (EnableUploads, self-hosted only) and Require plugin signature (RequirePluginSignature, must be disabled for uploads). A "Received invalid response from the server" error on upload usually means the maximum file size setting is too small; raise it and adjust proxy limits.

Install methods:
- App Marketplace (recommended): Product menu > App Marketplace > Install, then Configure or Enable. Always the latest compatible, signature-validated version.
- Upload: download the .tar.gz bundle (choose the platform-specific bundle, such as linux-amd64, or the larger universal one), then Plugins > Plugin Management > Upload Plugin and Enable it.
- mmctl: mmctl plugin marketplace install <id>; mmctl plugin add myplugin.tar.gz; mmctl plugin install-url https://example.com/myplugin.tar.gz; then mmctl plugin enable <id>. The id comes from the plugin.json manifest (for example com.mattermost.calls); mmctl plugin list shows installed plugins.

Installing does not enable. Enable and disable via the console or mmctl plugin enable/disable <id>; disabling removes the plugin from the UI but keeps it installed. Updating: pre-packaged plugins upgrade automatically when Automatic prepackaged plugins is on (default); Marketplace shows an Update option; uploads with the same ID overwrite; mmctl plugin add ... --force overwrites without confirmation, so test in staging.

Removal (console Remove or mmctl plugin delete <id>) keeps the plugin's configuration marked disabled, its key-value data and its bot accounts (deactivate those under Integrations > Bot Accounts). Reinstalling restores prior settings.

## Checked

Confirmed against the Install and manage plugins page: the gating settings and defaults, the upload error note, the three install methods and mmctl commands, enable and disable behaviour, the four update routes including --force, and what removal preserves. Nothing removed.

Method: docs-checked 2026-11-09 against the full administration-guide/configure/manage-plugins page (source rst from the mattermost/docs repo).

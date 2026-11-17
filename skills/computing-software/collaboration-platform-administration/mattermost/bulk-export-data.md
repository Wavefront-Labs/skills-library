---
id: computing-software.collaboration-platform-administration.mattermost.bulk-export-data
name: bulk-export-data
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [bulk-export, jsonl, mmctl-export, data-migration]
level: advanced
status: docs-checked
description: "Export a Mattermost server to a JSONL bulk-import file with mmctl export (including attachments) or the deprecated CLI command, and what data it covers."
sources: ["https://docs.mattermost.com/administration-guide/manage/bulk-export-tool.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bulk export

Moving data between Mattermost instances starts with exporting to a JSONL file in the bulk-loading format. It is useful when a proof-of-concept server's history should be kept on a production server.

Exported data types: teams; channels (public, private and direct); messages, replies and threads; reactions; users, their preferences (including pinned and saved messages), team and channel memberships and notification preferences; custom emoji; direct and group message channels with read state; roles; permissions schemes; and bot users. Not yet supported: exporting specific areas only, additional post types, file attachments in the export configuration, webhooks, bot messages, and deleted objects.

With mmctl (recommended):
1. Run mmctl export create --attachments to produce a full export including attachments.
2. Check progress with mmctl export job show.
3. When the job is successful, find the file name with mmctl export list, then fetch it with mmctl export download.

With the server CLI (deprecated since v6.0 in favour of mmctl export): from the install directory (/opt/mattermost by default) run sudo -u mattermost bin/mattermost export bulk file.json --all-teams, choosing a file name and an absolute or relative path. This command can read everything in the database.

Every export file starts with a Version object (type "version", version 1, optional info with generator, version, created timestamp and additional data) that tells you which bulk import format the file matches.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/manage/bulk-export-tool (data types, mmctl and CLI steps, Version object). Reworded the unsupported-items list to match the page.

Method: documentation only; no commands were run.

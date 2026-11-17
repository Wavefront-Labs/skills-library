---
id: computing-software.collaboration-platform-administration.mattermost.migrate-from-other-chat-platforms
name: migrate-from-other-chat-platforms
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [migration-planning, bulk-loading, etl, slack-import]
level: practitioner
status: docs-checked
description: "Choose a path for moving to Mattermost from Slack, Rocket.Chat, Jabber, Pidgin or bespoke messengers using bulk load, ETL tools or parallel running."
sources: ["https://docs.mattermost.com/administration-guide/onboard/migrating-to-mattermost.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Migrating from other chat platforms

The migration guide points to separate procedures per source.

- Slack and Rocket.Chat have their own dedicated migration guides.
- Jabber: a federal agency migration was done by BrightScout, who open sourced an ETL (extract, transform, load) tool for Mattermost.
- Pidgin: to keep Pidgin clients working against a Mattermost backend, use the same ETL tool for data and the Pidgin-Mattermost (purple-mattermost) plugin, which includes an installer for end user machines.
- Bespoke messengers: data formats are unpredictable, so options depend on whether the history matters.

If the data is vital:
1. Use the Mattermost bulk load tool to ETL from your system into Mattermost.
2. Use the BrightScout ETL framework to configure an adapter feeding the bulk load tool.
3. If you only recently left Slack for the bespoke tool, go back and import the old Slack data directly.
4. Export Flowdock, Campfire, Chatwork, Hall or CSV data into Slack format, then import from Slack into Mattermost.

If the data is not vital:
1. Run Mattermost in parallel with the old system until most workflows have moved.
2. Announce a hard switch after a period of parallel running; this is often driven by security concerns or end-of-life products.

## Checked

Confirmed against the Migration guide page: the Slack, Rocket.Chat, Jabber, Pidgin and bespoke messenger sections, including the four vital-data options and the two non-vital options. Removed the closing advice about announcements and account setup, which that page does not state.

Method: docs-checked 2026-11-09 against the full administration-guide/onboard/migrating-to-mattermost page (source rst from the mattermost/docs repo).

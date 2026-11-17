---
id: computing-software.collaboration-platform-administration.mattermost.system-statistics-reporting
name: system-statistics-reporting
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [statistics, reporting, team-statistics, viewer-role]
level: practitioner
status: docs-checked
description: "Read Mattermost system and team statistics, understand how each figure is counted, and give team admins read-only access to team stats."
sources: ["https://docs.mattermost.com/administration-guide/manage/statistics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# System and team statistics

Mattermost tracks users, posts and channels for the system and each team. Enterprise editions have advanced system statistics. For large deployments, some message totals and per-day figures are bounded by the MaxUsersForStatistics configuration value to protect performance. For deeper metrics see the Prometheus and Grafana performance monitoring setup.

System statistics (System Console > Reporting) sum across all teams:
- Total Users: active accounts, excluding deactivated accounts and single-channel guests.
- Single-channel Guests: active guests belonging to exactly one active channel; DMs and group messages do not matter and archived channels are excluded.
- Total Teams; Total Channels (public and private, including deleted, not DMs); Total Posts (including deleted and automated posts).
- Daily Active Users (viewed the site in the last 24 hours) and Monthly Active Users (last 30 days), both excluding bots.
- Graphs for posts per day, bot posts per day and active users with posts.

Self-hosted adds: Total Sessions (unexpired), Total Commands, Incoming and Outgoing Webhooks (active only), WebSocket Conns, Master DB Conns, Replica DB Conns, Total Playbooks and Playbook Runs, plus Channel Types and Posts/Files/Hashtags charts.

Team statistics (System Console > Team Statistics) cover one team and exclude direct message posts.

Troubleshooting: "Not enough data for a meaningful representation" or an endlessly loading page can be caused by an ad blocker; disable it to test.

Team admin access: edit the Viewer system role under User Management > System Roles, set Team Statistics to Read only, set System Statistics, Server Logs and all other privileges to No access, assign team admins under Assigned People and save. Add and remove people manually as team admins change.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/administration-guide/manage/statistics (system, advanced, team statistics, viewer role). Nothing removed.

Method: documentation only; no commands were run.

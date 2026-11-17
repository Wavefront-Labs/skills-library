---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.network-planner-qos
name: network-planner-qos
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [network-planner-qos]
level: advanced
status: draft
description: Plan bandwidth and mark media traffic.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network planner and QoS
**Goal:** Plan bandwidth and mark media traffic.

- Network planner in Teams admin center > Planning.
- Media ports UDP 3478-3481; DSCP markings: audio 46, video 34, sharing 18 (typical defaults, confirm).
- Use the Microsoft 365 connectivity test for local egress.
- Bypass proxies for Teams media endpoints.

## Gotchas
- DSCP is honoured only if your network preserves markings.
- Check the current Microsoft 365 endpoint list.

## Self-check
Connectivity test reports direct egress and low latency to the nearest edge.

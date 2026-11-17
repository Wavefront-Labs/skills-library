---
id: computing-software.rpa-and-low-code.uipath.uipath-time-queue-triggers
name: uipath-time-queue-triggers
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-triggers-robots, uipath-time-queue-triggers]
level: advanced
status: draft
description: "Start jobs automatically."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Schedule with time and queue triggers
**Goal:** Start jobs automatically.

- Time triggers use cron schedules and time zones; queue triggers start jobs when pending items exceed a threshold.
- Configure job priority and number of robots.
- Avoid overlapping runs of the same process unless intended.

## Gotchas
- Daylight-saving time shifts affect cron schedules in local time zones.

## Self-check
Trigger starts a job at the expected time.

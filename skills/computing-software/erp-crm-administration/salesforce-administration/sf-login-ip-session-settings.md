---
id: computing-software.erp-crm-administration.salesforce-administration.sf-login-ip-session-settings
name: sf-login-ip-session-settings
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-login-ip-session-settings]
level: practitioner
status: draft
description: "Limit where and how long users sign in."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Restrict login IPs and set session settings
**Goal:** Limit where and how long users sign in.

- Network Access trusted IP ranges, profile Login IP Ranges and Login Hours; Session Settings for timeout and lock sessions to IP.
- Connected App policies (IP relaxation, refresh token policy) for integrations.
- Review login history regularly.

## Gotchas
- Login IP ranges on profiles hard-block users outside the range.

## Self-check
Login from an out-of-range IP fails.

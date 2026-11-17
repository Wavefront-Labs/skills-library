---
id: computing-software.cloud-infrastructure-engineering.harbor.scheduled-scans
name: scheduled-scans
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [schedule-scans, scan-all, cron, interrogation-services, harbor]
level: intro
status: docs-checked
description: "Schedule Harbor to scan all artifacts hourly, daily, weekly or on a custom cron expression from Interrogation Services."
sources:
  - https://goharbor.io/docs/main/administration/vulnerability-scanning/schedule-scans/
  - https://goharbor.io/docs/main/administration/vulnerability-scanning/stop-scan/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Harbor can run a scan of all artifacts on a policy. You need a system administrator account.

1. Expand **Administration** and select **Interrogation Services**.
2. Select the **Vulnerability** tab and click **Edit** next to **Schedule to scan all**.
3. Choose how often to run:
   - **None**: no scans are scheduled.
   - **Hourly**: at the beginning of every hour.
   - **Daily**: at midnight every day.
   - **Weekly**: at midnight every Saturday.
   - **Custom**: a `cron` expression you supply.
4. Click **Save**.

Related behaviour: after you click **SCAN NOW** to create a scan-all request, the button text changes to **STOP SCAN** so you can cancel it. Scanning can be resource-consuming enough to slow other Harbor functions, which is why scans can be stopped.

## Checked

2026-11-03. The menu path, schedule options and Save step were read against the Harbor docs page Schedule Scans; the SCAN NOW and STOP SCAN behaviour against Stop Scan. Removed: the Cosign-signature scanning statement and the claim that Scan Now is unavailable during a scan (neither is on those pages).

Method: documentation only; no commands were run.

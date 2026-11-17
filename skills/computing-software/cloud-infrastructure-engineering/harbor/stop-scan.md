---
id: computing-software.cloud-infrastructure-engineering.harbor.stop-scan
name: stop-scan
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [stop-scan, stop-scan-all, scan-stopped-webhook, scanning, harbor]
level: practitioner
status: docs-checked
description: "Stop a running Harbor vulnerability scan or a scan-all job, and receive the Scanning stopped webhook."
sources:
  - https://goharbor.io/docs/main/administration/vulnerability-scanning/stop-scan/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scanning can be resource heavy enough that Harbor struggles with other work. From Harbor 2.4.0 you can stop scans from the web portal.

Individual artifact: a **STOP SCAN** button sits next to **SCAN**. After you click SCAN the **Vulnerabilities** field goes Queued, then Scanning. Click STOP SCAN while it shows Scanning, and the field soon changes to **Scan stopped**.

Scan all: there is no extra button. After you click **SCAN NOW** to create a scan-all request, the same button text changes to **STOP SCAN**. Click it to send a stop-all request. All stopped jobs show **Scan stopped** and any webhooks are sent.

Webhook for stops:
1. Log in and open the project.
2. **Webhooks** tab, **NEW WEBHOOK**.
3. Fill in the form and tick the **Scanning stopped** event.
4. Click **ADD**.

After that, stopping a scan on an artifact in that project delivers a webhook payload to the endpoint.

## Checked

2026-11-03. Version 2.4.0, STOP SCAN and SCAN NOW button behaviour, the Scan stopped status and the webhook steps were read against the Harbor docs page Stop Scan. Removed: the claim about completion events (not on the page); narrowed the click timing to the page's Scanning state.

Method: documentation only; no commands were run.

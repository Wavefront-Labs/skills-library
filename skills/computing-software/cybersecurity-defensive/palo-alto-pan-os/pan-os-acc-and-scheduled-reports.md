---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-acc-and-scheduled-reports
name: pan-os-acc-and-scheduled-reports
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [application-command-center, pan-os, acc, custom-reports, scheduled-reports, global-filter, log-viewer]
level: practitioner
status: draft
description: "Use the PAN-OS ACC, log filters and scheduled or API-driven reports to find top apps, users and threats."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/monitoring/use-the-application-command-center"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: answer "what is using the network and what is risky" quickly.

ACC (Application Command Center) tabs: Network Activity, Threat Activity, Blocked Activity, Tunnel Activity, GlobalProtect Activity. Pick a time frame (last hour up to 30 days, or custom), then use the Global Filter (click any value to add it) to pivot by application, user, source, destination, zone or rule.

Log search examples (Monitor > Logs > Traffic)
```
( addr.src in 10.1.1.5 ) and ( app eq ssl ) and ( action eq deny )
( rule eq 'allow-web' ) and ( bytes geq 1000000 )
```

Reports: Monitor > Reports has predefined and custom reports. Schedule a custom report (Monitor > Manage Custom Reports) and email it as PDF (Device > Server Profiles > Email, Monitor > PDF Reports > Email Scheduler). Generate through the API:
```
curl --cacert ca.pem -H "X-PAN-KEY: $KEY" "https://fw.example.com/api/?type=report&reporttype=dynamic&reportname=top-applications&async=yes"
```
Then poll with `type=report&action=get&job-id=<ID>` (confirm report names for your version).

Gotchas
- ACC data depends on log retention and, on a managed firewall, whether you are viewing local or Panorama logs.
- Reports are limited by log quotas; expanding retention needs disk.
- ACC hides blocked traffic unless you switch to the Blocked Activity tab.

## Verify
Open ACC with last 1 hour, confirm the top application matches `show session info` volume, and run one scheduled report manually (Run Now) to check email delivery.

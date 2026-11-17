---
id: computing-software.networking-hardware-and-wireless.check-point.application-control-and-url-filtering
name: application-control-and-url-filtering
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, application-control, url-filtering, custom-categories]
level: practitioner
status: draft
description: "Write Check Point Application Control and URL Filtering rules, with custom applications, categories and rule action Ask or Inform."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_ThreatPrevention_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_SecurityManagement_AdminGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Application Control and URL Filtering

- Enable the **Applications & URL Filtering** blade on the gateway and the policy layer. The gateway needs access to the Check Point ThreatCloud for categorization (internet access from the gateway, and DNS), or categorization falls to "Uncategorized".
- Rule columns: Source, Destination (Internet), Services & Applications (application, category or custom), Action: Accept, Drop, **Ask** (user acknowledges), **Inform** (a banner). Limit actions (bandwidth) are available.
```
mgmt_cli -r true add application-site-category name "Corp-Allowed" description "Allowed SaaS"
mgmt_cli -r true add application-site name "intranet-portal" primary-category "Corp-Allowed" url-list.1 "portal.corp.example"
mgmt_cli -r true add access-rule layer "Network" position top name "Block P2P" service.1 "Peer to Peer File Sharing" action "Drop" track.type "Log"
mgmt_cli -r true publish
```
- Put block rules for risky categories above generic Accept rules; the rule can use a *negate cell*.
- Without **HTTPS Inspection**, URL Filtering only sees SNI/hostname of TLS traffic, not paths; Application Control signatures for some SaaS also need decrypted traffic.
- URL categorisation is cached; "Update Categorization" can be forced from the user via UserCheck feedback or.
- Gotcha: default "Rule Base order": if Application Control sits in a separate ordered layer, ensure a layer-1 rule allows the traffic first (**Accept** in both).

Verify: browse a test URL such as the EICAR download page; the log shows `Application`, `Application Category`, and `Rule` fields. `fw ctl zdebug` is not needed; use `urlf_cli` if available (confirm).

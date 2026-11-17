---
id: computing-software.cloud-infrastructure-engineering.google-cloud.app-engine-firewall-rules
name: app-engine-firewall-rules
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, app-engine, app-engine-firewall-rules, gcloud-app-firewall-rules, ip-allowlist, ingress-settings]
level: practitioner
status: docs-checked
description: "Restrict App Engine traffic with the App Engine firewall: rule priorities, default rule, allowing Cloud Tasks/cron and health traffic, testing rules, and ingress settings."
sources: ["https://cloud.google.com/appengine/docs/standard/creating-firewalls", "https://cloud.google.com/sdk/gcloud/reference/app/firewall-rules", "https://cloud.google.com/appengine/docs/standard/application-security#ingress_controls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Engine firewall rules

The App Engine firewall filters by source IP range for all resources of the app (up to 1000 rules). Rules
have a unique priority from 1 (most important) upward; the **default** rule (priority 2147483647) applies to every request that matches no other rule and is evaluated last. A rule set to deny returns 403 Forbidden.

## Allowlist pattern
```bash
gcloud app firewall-rules create 100 --action=allow --source-range=203.0.113.0/24 --description="office"
gcloud app firewall-rules update default --action=deny
gcloud app firewall-rules list
gcloud app firewall-rules test-ip 198.51.100.7     # tests which rule applies
```
Before switching the default to deny, make sure every legitimate source has an allow rule, and test with `test-ip` first. Creating rules needs the App Engine Admin, Editor or Owner role.

## Ingress settings (complementary)
```bash
gcloud app services update default --ingress=internal-and-cloud-load-balancing
```
`all`, `internal-only`, `internal-and-cloud-load-balancing`. If you route through Cloud Load Balancing with a serverless NEG, ingress controls stop users bypassing the load balancer, Cloud Armor policies and SSL certificates via the App Engine URL.

## Gotchas
- Denied requests are rejected with 403 before they reach your app, and blocked traffic is not billed.
- Firewall rules apply to the whole App Engine application, not to one service.
- Up to 1000 rules per app.

## Verify
- [ ] `test-ip` for an unknown IP shows the default rule's action; the office IP matches its allow rule.

## Checked
2026-10-27. Confirmed against App Engine creating-firewalls page (1000 rules, priority 1 to 2147483647, default rule at 2147483647 evaluated last, deny returns 403, allow/deny lowercase values, required roles), application-security page (ingress controls, blocked traffic not billed) and mapping-custom-domains page (load balancer bypass); gcloud reference for app firewall-rules create, update, list, test-ip and app services update --ingress (all, internal-only, internal-and-cloud-load-balancing). Removed: default-rule ALLOW claim, internal cron/task source-address advice, X-Forwarded-For and logging claims, geo/WAF comparison.
Method: documentation only; no commands were run.

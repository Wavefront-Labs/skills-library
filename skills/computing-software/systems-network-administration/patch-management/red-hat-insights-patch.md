---
id: computing-software.systems-network-administration.patch-management.red-hat-insights-patch
name: red-hat-insights-patch
category: computing-software
field: systems-network-administration
product: patch-management
tags: [red-hat-insights, insights-patch, rhel, advisories, linux-patch-tooling, patch-management]
level: practitioner
status: draft
description: "Use Red Hat Insights Patch and Vulnerability services: register hosts, view applicable advisories, build remediation playbooks, and report patch status across RHEL fleets."
sources:
  - https://docs.redhat.com/en/documentation/red_hat_insights/1-latest/html/system_patching_using_ansible_playbooks_via_remediations/index
  - https://docs.redhat.com/en/documentation/red_hat_insights/1-latest/html-single/system_patching_using_patch/index
  - https://docs.redhat.com/en/documentation/red_hat_insights/1-latest/html/assessing_and_monitoring_security_vulnerabilities_on_rhel_systems/index
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Red Hat Insights Patch

Insights (console.redhat.com) is included with RHEL subscriptions. **Patch** shows applicable advisories (RHSA/RHBA/RHEA) per system; **Vulnerability** maps CVEs with exploit/known-exploited flags; **Remediations** generates Ansible playbooks.

## Register
```sh
rhc connect --activation-key <key> --organization <org-id>     # RHEL 8.6+/9 (connects Insights + remote host config)
# or legacy
subscription-manager register --activationkey <key> --org <org>
insights-client --register
insights-client --check-results
```
Data upload runs daily via `insights-client.timer`; run `insights-client` after patching to refresh.

## Patch service
- Advisories view: filter by type Security, severity, publish date; see affected systems.
- Systems view: per-host applicable advisories and packages.
- **Patch templates** (content templates) pin systems to repository content as of a date, giving ring-like staging without Satellite.
- API: `GET https://console.redhat.com/api/patch/v3/advisories?filter[advisory_type_name]=security` (token via service account).

## Remediate
1. Select advisories + systems > Remediate > create/add to a playbook.
2. Run via Remote Host Configuration (rhc + Satellite/Cloud Connector) from the console, or download and run with Ansible.
3. Playbooks include an optional reboot task; set as needed.

## Vulnerability
Filter "Known exploit" and "Security rules"; CVEs with Insights security rules check config conditions (not just version), reducing false positives.

## Gotchas
- Systems behind proxies need `proxy` configured in `/etc/insights-client/insights-client.conf` or rhc config.
- Stale systems (not checked in for days) still show; filter by last seen.
- Satellite-managed hosts can report to Insights via Satellite's Insights plugin; avoid duplicate registrations.

## Verify
After remediation and `insights-client` upload, applicable security advisories count is zero for the target group; Patch report exported for the change record.
